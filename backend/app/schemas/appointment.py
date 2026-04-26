from pydantic import BaseModel
from datetime import date, time, datetime

class AppointmentCreate(BaseModel):
    slot_id: int


class AppointmentResponse(BaseModel):
    id: int
    slot_id: int
    doctor_id: int
    patient_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class AppointmentDetail(BaseModel):
    id: int
    doctor_id: int
    slot_id: int
    status: str
    date: date
    time: time
    created_at: datetime

    class Config:
        from_attributes = True

class DoctorAppointmentDetail(BaseModel):
    id: int
    patient_id: int
    slot_id: int
    status: str
    date: date
    time: time
    created_at: datetime

    class Config:
        from_attributes = True