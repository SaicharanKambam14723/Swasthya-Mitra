from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from app.db.database import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    slot_id = Column(Integer, ForeignKey("slots.id"), nullable=False)

    status = Column(String, default="booked")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # 🔥 RELATIONSHIPS
    patient = relationship("User", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")
    slot = relationship("Slot", back_populates="appointments")