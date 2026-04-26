from pydantic import BaseModel
from datetime import date, time

class SlotCreate(BaseModel):
    date: date
    time: time


class SlotResponse(BaseModel):
    id: int
    date: date
    time: time
    status: str

    class Config:
        from_attributes = True

class SlotGenerate(BaseModel):
    date: date
    start_time: time
    end_time: time
    interval: int