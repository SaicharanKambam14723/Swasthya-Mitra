from sqlalchemy import Column, Integer, ForeignKey, Date, Time
from app.db.database import Base

class Slot(Base):
    __tablename__ = "slots"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)

    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)