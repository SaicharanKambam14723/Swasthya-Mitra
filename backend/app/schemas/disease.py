from pydantic import BaseModel

class DiseaseCreate(BaseModel):
    name: str
    description: str
    severity: str
    category: str


class DiseaseResponse(BaseModel):
    id: int
    name: str
    description: str
    severity: str
    category: str

    class Config:
        from_attributes = True