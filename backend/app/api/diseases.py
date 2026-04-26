from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.disease import Disease
from app.schemas.disease import DiseaseCreate

router = APIRouter()


@router.post("/")
def create_disease(
    data: DiseaseCreate,
    db: Session = Depends(get_db)
):
    disease = Disease(**data.dict())

    db.add(disease)
    db.commit()
    db.refresh(disease)

    return {
        "success": True,
        "data": disease,
        "message": "Disease added"
    }


@router.get("/")
def get_diseases(db: Session = Depends(get_db)):
    diseases = db.query(Disease).all()

    return {
        "success": True,
        "data": diseases,
        "message": "Diseases fetched"
    }