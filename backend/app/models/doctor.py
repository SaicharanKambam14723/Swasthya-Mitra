from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    specialization = Column(String, nullable=False)
    experience = Column(Integer, nullable=False)
    hospital_name = Column(String, nullable=False)