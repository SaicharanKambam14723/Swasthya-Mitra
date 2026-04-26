from pydantic import BaseModel
from datetime import date, time

class AppointmentCreate(BaseModel):
    slot_id: int


class AppointmentResponse(BaseModel):
    id: int
    slot_id: int
    doctor_id: int
    patient_id: int
    status: str

    class Config:
        from_attributes = True


class AppointmentDetail(BaseModel):
    id: int
    doctor_id: int
    slot_id: int
    status: str
    date: date
    time: time

    class Config:
        from_attributes = True

class DoctorAppointmentDetail(BaseModel):
    id: int
    patient_id: int
    slot_id: int
    status: str
    date: date
    time: time

    class Config:
        from_attributes = True