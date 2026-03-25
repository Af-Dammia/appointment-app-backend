# app/scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.email_service import send_reminder_email
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models import Appointment
from app.database import SessionLocal
import pytz  # for timezone handling

# Berlin timezone
BERLIN = pytz.timezone("Europe/Berlin")

scheduler = AsyncIOScheduler()

def get_upcoming_appointments(hours_ahead: float = 0.0833):
    """
    Fetch appointments that are within the next `hours_ahead` hours
    in Berlin timezone.
    """
    db: Session = SessionLocal()
    
    # Current time in Berlin
    now_berlin = datetime.now(BERLIN)
    upcoming_time = now_berlin + timedelta(hours=hours_ahead)
    
    # Convert Berlin time to naive UTC for database comparison if stored in UTC
    now_utc = now_berlin.astimezone(pytz.UTC).replace(tzinfo=None)
    upcoming_utc = upcoming_time.astimezone(pytz.UTC).replace(tzinfo=None)

    appointments = (
        db.query(Appointment)
        .filter(Appointment.appointment_date >= now_utc)
        .filter(Appointment.appointment_date <= upcoming_utc)
        .all()
    )
    db.close()
    return appointments

async def check_and_send_reminders():
    """
    Check upcoming appointments and send email reminders.
    """
    upcoming = get_upcoming_appointments(hours_ahead=1)
    for appointment in upcoming:
        if appointment.user_email:
            # Send email with Berlin time in message
            appointment_time_berlin = appointment.appointment_date.replace(tzinfo=pytz.UTC).astimezone(BERLIN)
            await send_reminder_email(
                appointment.user_email,
                appointment.title,
                appointment_time_berlin.strftime("%Y-%m-%d %H:%M")
            )

def start_scheduler():
    # Check every minute
    scheduler.add_job(check_and_send_reminders, "interval", minutes=1)
    scheduler.start()