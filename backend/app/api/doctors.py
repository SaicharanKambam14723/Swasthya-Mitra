from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.doctor import Doctor
from app.schemas.doctor import DoctorCreate, DoctorResponse
from app.core.deps import get_current_user, require_role
from typing import Optional, List
from app.models.user import User
from app.schemas.doctor import DoctorDetailResponse
from fastapi import Query
from fastapi import Path

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_doctor(
    data: DoctorCreate,
    db: Session = Depends(get_db),
    user = Depends(require_role("doctor"))   # 🔥 FIX
):
    # ❌ Prevent duplicate profile
    existing = db.query(Doctor).filter(Doctor.user_id == user.id).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Doctor profile already exists"
        )

    doctor = Doctor(
        user_id=user.id,
        specialization=data.specialization,
        experience=data.experience
    )

    db.add(doctor)
    db.commit()
    db.refresh(doctor)

    return {
        "success": True,
        "data": doctor,
        "message": "Doctor profile created"
    }

@router.get("/")
def get_doctors(
    specialization: Optional[str] = None,
    min_experience: Optional[int] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    query = db.query(Doctor)
    query = query.order_by(Doctor.experience.desc())

    if specialization:
        query = query.filter(Doctor.specialization.ilike(f"%{specialization}%"))

    if min_experience:
        query = query.filter(Doctor.experience >= min_experience)

    doctors = query.offset(skip).limit(limit).all()

    return {
        "success": True,
        "data": doctors,
        "message": "Doctors fetched successfully"
    }

@router.get("/me")
def get_my_doctor_profile(
    db: Session = Depends(get_db),
    user = Depends(require_role("doctor"))
):
    doctor = db.query(Doctor).filter(Doctor.user_id == user.id).first()

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor profile not found")

    return {
        "success": True,
        "data": doctor,
        "message": "Doctor profile fetched"
    }

@router.get("/{doctor_id}")
def get_doctor(
    doctor_id: int,
    db: Session = Depends(get_db)
):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return {
        "success": True,
        "data": doctor,
        "message": "Doctor fetched"
    }