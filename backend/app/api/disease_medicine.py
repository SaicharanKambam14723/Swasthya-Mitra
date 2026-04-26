from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.disease import Disease
from app.models.medicine import Medicine

router = APIRouter()


# 🔗 LINK MEDICINE TO DISEASE
@router.post("/link")
def link_medicine_to_disease(
    disease_id: int,
    medicine_id: int,
    db: Session = Depends(get_db)
):
    disease = db.query(Disease).filter(Disease.id == disease_id).first()
    medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()

    if not disease or not medicine:
        raise HTTPException(status_code=404, detail="Disease or Medicine not found")

    disease.medicines.append(medicine)
    db.commit()

    return {
        "success": True,
        "message": "Medicine linked to disease"
    }


# 📥 GET MEDICINES FOR A DISEASE
@router.get("/{disease_id}")
def get_medicines_for_disease(
    disease_id: int,
    db: Session = Depends(get_db)
):
    disease = db.query(Disease).filter(Disease.id == disease_id).first()

    if not disease:
        raise HTTPException(status_code=404, detail="Disease not found")

    return {
        "success": True,
        "data": disease.medicines,
        "message": "Medicines fetched"
    }