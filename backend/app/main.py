from fastapi import FastAPI
from app.db.database import Base, engine
from app.models.user import User
from app.core.security import create_access_token
from app.api.auth import router as auth_router
from app.core.deps import get_current_user
from fastapi import Depends
from app.models.doctor import Doctor
from app.api.doctors import router as doctor_router
from app.models.slot import Slot
from app.models.appointment import Appointment
from app.api.appointments import router as appointment_router
from app.api.slots import router as slot_router

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])

app.include_router(slot_router, prefix="/slots", tags=["Slots"])

app.include_router(appointment_router, prefix="/appointments", tags=["Appointments"])

app.include_router(doctor_router, prefix="/doctors", tags=["Doctors"])

@app.get("/")
def root():
    return {"message": "Backend running clean 🚀"}

@app.get("/protected")
def protected_route(user=Depends(get_current_user)):
    return {"message": "You are authenticated", "user": user}