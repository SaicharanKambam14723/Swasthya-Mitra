from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.disease import Disease

router = APIRouter()


# 🔍 GET MEDICINES BY DISEASE (AI READY)
@router.get("/diseases/{disease_id}/medicines")
def get_medicines_by_disease(
    disease_id: int,
    db: Session = Depends(get_db)
):
    disease = db.query(Disease).filter(Disease.id == disease_id).first()

    if not disease:
        raise HTTPException(status_code=404, detail="Disease not found")

    allopathic = []
    ayurvedic = []

    for med in disease.medicines:
        med_data = {
            "id": med.id,
            "name": med.name,
            "description": med.description,
            "dosage": med.dosage
        }

        if med.type == "allopathic":
            allopathic.append(med_data)
        elif med.type == "ayurvedic":
            ayurvedic.append(med_data)

    return {
        "success": True,
        "data": {
            "disease": disease.name,
            "severity": disease.severity,
            "allopathic": allopathic,
            "ayurvedic": ayurvedic
        },
        "message": "Medicines fetched successfully"
    }