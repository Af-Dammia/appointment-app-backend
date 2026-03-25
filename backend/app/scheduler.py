# app/scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.email_service import send_reminder_email
from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timedelta
from app.models import Appointment
from app.database import SessionLocal
import pytz

BERLIN = pytz.timezone("Europe/Berlin")

scheduler = AsyncIOScheduler()

def get_upcoming_appointments(db: Session, hours_ahead: float = 0.0833):
    now = datetime.utcnow()
    upcoming_time = now + timedelta(hours=hours_ahead)

    return (
        db.query(Appointment)
        .options(joinedload(Appointment.user))
        .filter(Appointment.appointment_date >= now)
        .filter(Appointment.appointment_date <= upcoming_time)
        .filter(Appointment.reminder_sent == False)
        .all()
    )

async def check_and_send_reminders():
    db = SessionLocal()

    upcoming = get_upcoming_appointments(db, hours_ahead=0.0833)  # 5 min test

    for appointment in upcoming:
        if appointment.user and appointment.user.email:
            appointment_time_berlin = appointment.appointment_date.replace(tzinfo=pytz.UTC).astimezone(BERLIN)

            await send_reminder_email(
                appointment.user.email,
                appointment.title,
                appointment_time_berlin.strftime("%Y-%m-%d %H:%M")
            )

            appointment.reminder_sent = True

    db.commit()
    db.close()

def start_scheduler():
    scheduler.add_job(check_and_send_reminders, "interval", minutes=1)
    scheduler.start()