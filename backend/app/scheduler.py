# app/scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.email_service import send_reminder_email

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models import Appointment
from app.database import SessionLocal

scheduler = AsyncIOScheduler()

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

def start_scheduler():
    scheduler.add_job(check_and_send_reminders, "interval", minutes=1)
    scheduler.start()

async def check_and_send_reminders():
    upcoming = await get_upcoming_appointments()
    for appointment in upcoming:
        await send_reminder_email(
            appointment.user_email,
            appointment.title,
            appointment.date.strftime("%Y-%m-%d %H:%M")
        )


