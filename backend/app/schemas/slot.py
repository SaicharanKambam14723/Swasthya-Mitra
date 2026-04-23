from pydantic import BaseModel
from datetime import date, time

class SlotCreate(BaseModel):
    date: date
    time: time


class SlotResponse(BaseModel):
    id: int
    date: date
    time: time

    class Config:
        from_attributes = True