from app.db.database import Base
from sqlalchemy import Column, Integer, Date, Time, String, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint

class Slot(Base):
    __tablename__ = "slots"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    status = Column(String, default="available")

    # 🔥 RELATIONSHIPS
    doctor = relationship("Doctor", back_populates="slots")
    appointments = relationship("Appointment", back_populates="slot")

    # Indexes
    __table_args__ = (
        UniqueConstraint("doctor_id", "date", "time", name="uq_slot_doctor_date_time"),
    )