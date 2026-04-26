from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.medicine import Medicine
from app.schemas.medicine import MedicineCreate

router = APIRouter()


@router.post("/")
def create_medicine(
    data: MedicineCreate,
    db: Session = Depends(get_db)
):
    medicine = Medicine(**data.dict())

    db.add(medicine)
    db.commit()
    db.refresh(medicine)

    return {
        "success": True,
        "data": medicine,
        "message": "Medicine added"
    }


@router.get("/")
def get_medicines(db: Session = Depends(get_db)):
    medicines = db.query(Medicine).all()

    return {
        "success": True,
        "data": medicines,
        "message": "Medicines fetched"
    }