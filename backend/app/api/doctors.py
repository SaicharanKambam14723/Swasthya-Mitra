from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.doctor import Doctor
from app.schemas.doctor import DoctorCreate, DoctorResponse
from app.core.deps import get_current_user
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
    user=Depends(get_current_user),
):
    if user.role != "doctor":
        raise HTTPException(status_code=403, detail="Only doctors allowed")

    doctor = Doctor(
        user_id=user.id,
        specialization=data.specialization,
        experience=data.experience,
        hospital_name=data.hospital_name,
    )

    db.add(doctor)
    db.commit()
    db.refresh(doctor)

    return {"message": "Doctor profile created"}

@router.get("/", response_model=List[DoctorResponse])
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

    return query.offset(skip).limit(limit).all()

@router.get("/me")
def get_my_doctor_profile(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user.role != "doctor":
        raise HTTPException(status_code=403, detail="Only doctors allowed")

    doctor = db.query(Doctor).filter(Doctor.user_id == user.id).first()

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor profile not found")

    return {
        "id": doctor.id,
        "specialization": doctor.specialization,
        "experience": doctor.experience,
        "hospital_name": doctor.hospital_name,
        "name": user.name,
        "email": user.email,
    }

@router.get("/{doctor_id}", response_model=DoctorDetailResponse)
def get_doctor_by_id(
    doctor_id: int,
    db: Session = Depends(get_db)
):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    user = db.query(User).filter(User.id == doctor.user_id).first()

    return {
        "id": doctor.id,
        "specialization": doctor.specialization,
        "experience": doctor.experience,
        "hospital_name": doctor.hospital_name,
        "name": user.name,
        "email": user.email,
    }