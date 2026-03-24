from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models import Appointment
from app.database import SessionLocal

# PostgreSQL credentials
#DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/appointment_db"

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
# Create engine
engine = create_engine(DATABASE_URL)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_upcoming_appointments(hours_ahead: int = 1):
    """
    Fetch appointments that are within the next `hours_ahead` hours.
    """
    db: Session = SessionLocal()
    now = datetime.utcnow()
    upcoming_time = now + timedelta(hours=hours_ahead)
    
    appointments = (
        db.query(Appointment)
        .filter(Appointment.appointment_date >= now)
        .filter(Appointment.appointment_date <= upcoming_time)
        .all()
    )
    db.close()
    return appointments