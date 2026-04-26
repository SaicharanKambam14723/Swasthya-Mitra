from sqlalchemy import Column, Integer, String
from app.db.database import Base
from sqlalchemy.orm import relationship
from app.models.disease_medicine import DiseaseMedicine

class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    diseases = relationship(
        "Disease",
        secondary="disease_medicine",
        back_populates="medicines"
    )
    type = Column(String, nullable=False)  # allopathic / ayurvedic
    description = Column(String)
    dosage = Column(String)   # e.g., "Twice daily after meals"