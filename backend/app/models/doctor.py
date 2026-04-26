from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base
from sqlalchemy.orm import relationship


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)

    specialization = Column(String, nullable=False)
    experience = Column(Integer, nullable=False)

    # 🔥 RELATIONSHIPS
    appointments = relationship("Appointment", back_populates="doctor")
    slots = relationship("Slot", back_populates="doctor")