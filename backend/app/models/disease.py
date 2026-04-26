from sqlalchemy import Column, Integer, String
from app.db.database import Base
from app.models.disease_medicine import DiseaseMedicine
from sqlalchemy.orm import relationship

class Disease(Base):
    __tablename__ = "diseases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    severity = Column(String)   # low / medium / high
    category = Column(String)   # e.g., viral, bacterial

    medicines = relationship(
        "Medicine",
        secondary="disease_medicine",
        back_populates="diseases"
    )