from sqlalchemy import Column, Integer, ForeignKey
from app.db.database import Base

class DiseaseMedicine(Base):
    __tablename__ = "disease_medicine"

    id = Column(Integer, primary_key=True, index=True)
    disease_id = Column(Integer, ForeignKey("diseases.id"), nullable=False)
    medicine_id = Column(Integer, ForeignKey("medicines.id"), nullable=False)