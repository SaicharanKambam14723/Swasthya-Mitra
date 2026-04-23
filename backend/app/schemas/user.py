from pydantic import BaseModel, EmailStr, Field
from typing import Literal


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=50)
    role: Literal["patient", "doctor"]

class UserLogin(BaseModel):
    email: EmailStr
    password: str