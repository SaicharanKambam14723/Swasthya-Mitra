from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from typing import List, Optional
from fastapi import Query
from app.models.slot import Slot
from app.models.doctor import Doctor
from app.schemas.slot import SlotCreate, SlotResponse
from app.core.deps import get_current_user
from datetime import datetime, timedelta
from datetime import date, time
from app.db.database import get_db
from app.schemas.slot import SlotGenerate

router = APIRouter()

@router.post("/")
def create_slot(
    data: SlotCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if user.role != "doctor":
        raise HTTPException(status_code=403, detail="Only doctors allowed")

    doctor = db.query(Doctor).filter(Doctor.user_id == user.id).first()

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor profile not found")

    # prevent duplicate slot
    existing = db.query(Slot).filter(
        Slot.doctor_id == doctor.id,
        Slot.date == data.date,
        Slot.time == data.time
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Slot already exists")

    slot = Slot(
        doctor_id=doctor.id,
        date=data.date,
        time=data.time,
        status="available"
    )

    db.add(slot)
    db.commit()
    db.refresh(slot)

    return {"message": "Slot created"}


@router.get("/{doctor_id}", response_model=List[SlotResponse])
def get_slots(
    doctor_id: int,
    date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    now = datetime.now()

    query = db.query(Slot).filter(
        Slot.doctor_id == doctor_id,
        Slot.status == "available"
    )

    # 📅 Filter by date if provided
    if date:
        query = query.filter(Slot.date == date)
    else:
        # 🔥 Only future slots
        query = query.filter(
            (Slot.date > now.date()) |
            ((Slot.date == now.date()) & (Slot.time > now.time()))
        )

    # 🔽 Sort properly
    slots = query.order_by(Slot.date, Slot.time).all()

    return slots

@router.post("/generate")
def generate_slots(
    data: SlotGenerate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user.role != "doctor":
        raise HTTPException(status_code=403, detail="Only doctors can generate slots")

    doctor = db.query(Doctor).filter(Doctor.user_id == user.id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor profile not found")

    start_dt = datetime.combine(data.date, data.start_time)
    end_dt = datetime.combine(data.date, data.end_time)

    now = datetime.now()

    if data.date < now.date():
        raise HTTPException(status_code=400, detail="Cannot create slots for past dates")

    if data.date == now.date() and data.start_time <= now.time():
        raise HTTPException(status_code=400, detail="Start time must be in future")

    if start_dt >= end_dt:
        raise HTTPException(status_code=400, detail="Start time must be before end time")

    if data.interval <= 0:
        raise HTTPException(status_code=400, detail="Interval must be greater than 0")

    total_minutes = (end_dt - start_dt).total_seconds() / 60
    if total_minutes / data.interval > 100:
        raise HTTPException(status_code=400, detail="Too many slots requested")

    slots_created = []
    current = start_dt

    while current < end_dt:
        slot_time = current.time()

        exists = db.query(Slot).filter(
            Slot.doctor_id == doctor.id,
            Slot.date == data.date,
            Slot.time == slot_time
        ).first()

        if not exists:
            new_slot = Slot(
                doctor_id=doctor.id,
                date=data.date,
                time=slot_time,
                status="available"   # ✅ 3D FIX
            )
            db.add(new_slot)
            slots_created.append(str(slot_time))

        current += timedelta(minutes=data.interval)

    db.commit()

    return {
        "message": f"{len(slots_created)} slots created",
        "slots": slots_created
    }