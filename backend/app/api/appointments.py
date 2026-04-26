from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.appointment import Appointment
from app.models.slot import Slot
from app.models.doctor import Doctor
from app.schemas.appointment import AppointmentCreate
from app.core.deps import get_current_user

router = APIRouter()

@router.post("/")
def book_appointment(
    data: AppointmentCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user.role != "patient":
        raise HTTPException(status_code=403, detail="Only patients can book")

    # 🔒 LOCK SLOT ROW (CRITICAL)
    slot = db.query(Slot).filter(Slot.id == data.slot_id).with_for_update().first()

    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")

    # ❌ Double booking prevention
    if slot.status != "available":
        raise HTTPException(status_code=400, detail="Slot already booked")

    doctor = db.query(Doctor).filter(Doctor.id == slot.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    try:
        # ✅ Create appointment
        appointment = Appointment(
            patient_id=user.id,
            doctor_id=doctor.id,
            slot_id=slot.id,
            status="booked"
        )

        # 🔒 LOCK SLOT
        slot.status = "booked"

        db.add(appointment)
        db.commit()
        db.refresh(appointment)

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Booking failed")

    return {
        "message": "Appointment booked successfully",
        "appointment_id": appointment.id
    }


@router.put("/cancel/{appointment_id}")
def cancel_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    # 🔐 Only patient
    if user.role != "patient":
        raise HTTPException(status_code=403, detail="Only patients can cancel")

    # 🔍 Get appointment
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    # ❌ Ownership check
    if appointment.patient_id != user.id:
        raise HTTPException(status_code=403, detail="Not your appointment")

    # ❌ Already cancelled
    if appointment.status == "cancelled":
        raise HTTPException(status_code=400, detail="Already cancelled")

    # 🔍 Get slot
    slot = db.query(Slot).filter(Slot.id == appointment.slot_id).first()

    try:
        # 🔄 Update status
        appointment.status = "cancelled"

        # 🔓 Unlock slot
        if slot:
            slot.status = "available"

        db.commit()

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Cancellation failed")

    return {"message": "Appointment cancelled successfully"}

@router.get("/my", response_model=dict)
def get_my_appointments(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user.role != "patient":
        raise HTTPException(status_code=403, detail="Only patients allowed")

    now = datetime.now()

    appointments = db.query(Appointment).filter(
        Appointment.patient_id == user.id
    ).all()

    upcoming = []
    past = []

    for appt in appointments:
        slot = db.query(Slot).filter(Slot.id == appt.slot_id).first()

        if not slot:
            continue

        item = {
            "id": appt.id,
            "doctor_id": appt.doctor_id,
            "slot_id": appt.slot_id,
            "status": appt.status,
            "date": slot.date,
            "time": slot.time
        }

        # 📊 Split upcoming vs past
        if (slot.date > now.date()) or (
            slot.date == now.date() and slot.time > now.time()
        ):
            upcoming.append(item)
        else:
            past.append(item)

    return {
        "upcoming": sorted(upcoming, key=lambda x: (x["date"], x["time"])),
        "past": sorted(past, key=lambda x: (x["date"], x["time"]), reverse=True)
    }

@router.get("/doctor", response_model=list)
def get_doctor_appointments(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    # 🔐 Only doctor
    if user.role != "doctor":
        raise HTTPException(status_code=403, detail="Only doctors allowed")

    # 🔍 Get doctor profile
    doctor = db.query(Doctor).filter(Doctor.user_id == user.id).first()

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor profile not found")

    appointments = db.query(Appointment).filter(
        Appointment.doctor_id == doctor.id
    ).all()

    result = []

    for appt in appointments:
        slot = db.query(Slot).filter(Slot.id == appt.slot_id).first()

        if not slot:
            continue

        result.append({
            "id": appt.id,
            "patient_id": appt.patient_id,
            "slot_id": appt.slot_id,
            "status": appt.status,
            "date": slot.date,
            "time": slot.time
        })

    # 🔽 Sort by date & time
    result = sorted(result, key=lambda x: (x["date"], x["time"]))

    return result