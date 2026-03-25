# app/scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.email_service import send_reminder_email
from app.models import Appointment, User
from app.database import SessionLocal

scheduler = AsyncIOScheduler()


def get_upcoming_appointments():
    db: Session = SessionLocal()
    now = datetime.utcnow()

    one_hour = now + timedelta(minutes=1)
    window = now + timedelta(minutes=2)

    appointments = (
        db.query(Appointment)
        .filter(Appointment.appointment_date >= one_hour)
        .filter(Appointment.appointment_date <= window)
        .filter(Appointment.reminder_sent == False)
        .all()
    )

    db.close()
    return appointments


def start_scheduler():
    scheduler.add_job(check_and_send_reminders, "interval", minutes=1)
    scheduler.start()


async def check_and_send_reminders():
    db = SessionLocal()

    appointments = get_upcoming_appointments() 

    for appointment in appointments:
        user = db.query(User).filter(User.id == appointment.user_id).first()

        if user:
            await send_reminder_email(
                user.email,
                appointment.title,
                appointment.appointment_date.strftime("%Y-%m-%d %H:%M")
            )

            appointment.reminder_sent = True  # prevent duplicates

    db.commit()
    db.close()