from pydantic import BaseModel

class MedicineCreate(BaseModel):
    name: str
    type: str
    description: str
    dosage: str


class MedicineResponse(BaseModel):
    id: int
    name: str
    type: str
    description: str
    dosage: str

    class Config:
        from_attributes = True