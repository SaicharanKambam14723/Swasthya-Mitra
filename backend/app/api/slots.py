from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from typing import List
from fastapi import Query
from app.db.database import SessionLocal
from app.models.slot import Slot
from app.models.doctor import Doctor
from app.schemas.slot import SlotCreate, SlotResponse
from app.core.deps import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
        time=data.time
    )

    db.add(slot)
    db.commit()
    db.refresh(slot)

    return {"message": "Slot created"}


@router.get("/{doctor_id}", response_model=List[SlotResponse])
def get_slots(
    doctor_id: int,
    date: str = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Slot).filter(Slot.doctor_id == doctor_id)

    if date:
        query = query.filter(Slot.date == date)

    return query.all()