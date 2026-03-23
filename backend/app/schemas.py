from pydantic import BaseModel, SecretStr, constr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: constr(min_length=6, max_length=72)

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# 📅 Appointment Schemas (ADD THESE)
class AppointmentCreate(BaseModel):
    title: str
    description: Optional[str] = None
    appointment_date: datetime


class AppointmentResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    user_id: Optional[int]
    date_time: datetime
    appointment_date: datetime

    class Config:
        from_attributes = True  # important for SQLAlchemy