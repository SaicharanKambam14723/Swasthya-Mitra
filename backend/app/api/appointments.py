from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.appointment import Appointment
from app.models.slot import Slot
from app.models.doctor import Doctor
from app.schemas.appointment import AppointmentCreate
from app.core.deps import get_current_user, require_role

router = APIRouter()

@router.post("/")
def book_appointment(
    slot_id: int,
    db: Session = Depends(get_db),
    user = Depends(require_role("patient"))   # 🔥 ONLY PATIENT
):
    # 🔍 Get slot
    slot = db.query(Slot).filter(Slot.id == slot_id).first()

    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")

    # ❌ Prevent double booking
    updated = db.query(Slot).filter(
        Slot.id == slot_id,
        Slot.status == "available"
    ).update({"status": "booked"})

    if updated == 0:
        raise HTTPException(status_code=400, detail="Slot already booked")

    # ✅ Create appointment
    appointment = Appointment(
        patient_id=user.id,
        doctor_id=slot.doctor_id,
        slot_id=slot.id,
        status="booked"
    )

    # 🔒 Lock slot
    slot.status = "booked"

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    return {
        "success": True,
        "data": appointment,
        "message": "Appointment booked successfully"
    }

@router.put("/{appointment_id}/cancel")
def cancel_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    user = Depends(require_role("patient"))   # 🔥 ONLY PATIENT
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    # 🔒 OWNERSHIP CHECK (CRITICAL)
    if appointment.patient_id != user.id:
        raise HTTPException(status_code=403, detail="Not your appointment")

    # ❌ Prevent invalid state
    if appointment.status == "cancelled":
        raise HTTPException(status_code=400, detail="Already cancelled")

    # 🔄 Update status
    appointment.status = "cancelled"

    # 🔓 Free slot
    slot = db.query(Slot).filter(Slot.id == appointment.slot_id).first()
    if slot:
        slot.status = "available"

    db.commit()

    return {
        "success": True,
        "data": None,
        "message": "Appointment cancelled"
    }

@router.get("/me")
def get_my_appointments(
    db: Session = Depends(get_db),
    user = Depends(require_role("patient"))
):
    appointments = db.query(Appointment).filter(
        Appointment.patient_id == user.id
    ).all()

    return {
        "success": True,
        "data": appointments,
        "message": "Your appointments fetched"
    }

@router.get("/doctor")
def get_doctor_appointments(
    db: Session = Depends(get_db),
    user = Depends(require_role("doctor"))
):
    doctor = db.query(Doctor).filter(
        Doctor.user_id == user.id
    ).first()

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    appointments = db.query(Appointment).filter(
        Appointment.doctor_id == doctor.id
    ).all()

    return {
        "success": True,
        "data": appointments,
        "message": "Doctor appointments fetched"
    }