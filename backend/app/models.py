from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from datetime import datetime
from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    appointment_date = Column(DateTime, nullable=False)
    date_time = Column(TIMESTAMP, default=datetime.utcnow)