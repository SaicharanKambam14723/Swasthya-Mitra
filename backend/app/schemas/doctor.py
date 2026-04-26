from pydantic import BaseModel, Field

class DoctorCreate(BaseModel):
    specialization: str = Field(..., min_length=2)
    experience: int = Field(..., ge=0)

class DoctorResponse(BaseModel):
    id: int
    specialization: str
    experience: int

    class Config:
        from_attributes = True

class DoctorDetailResponse(BaseModel):
    id: int
    specialization: str
    experience: int

    name: str
    email: str

    class Config:
        from_attributes = True