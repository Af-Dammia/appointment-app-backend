# app/scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timedelta, timezone
from app.models import Appointment
from app.database import SessionLocal
from app.email_service import send_reminder_email
import pytz
import asyncio

# Berlin timezone for emails
BERLIN = pytz.timezone("Europe/Berlin")

scheduler = AsyncIOScheduler()

def get_upcoming_appointments(db: Session, minutes_ahead: int = 60):
    """
    Fetch appointments that will occur within the next X minutes
    and haven't received a reminder yet.
    """
    now_utc = datetime.now(timezone.utc)
    upcoming_utc = now_utc + timedelta(minutes=minutes_ahead)

    return (
        db.query(Appointment)
        .options(joinedload(Appointment.user))
        .filter(Appointment.reminder_sent == False)
        .filter(Appointment.appointment_date >= now_utc)
        .filter(Appointment.appointment_date <= upcoming_utc)
        .all()
    )


async def check_and_send_reminders(test_minutes: int = 5):
    """
    Scheduler job: sends reminders for appointments within the next X minutes.
    By default, test_minutes=5 for testing; set to 60 for production.
    """
    db = SessionLocal()
    try:
        upcoming_appointments = get_upcoming_appointments(db, minutes_ahead=test_minutes)

        if upcoming_appointments:
            print(f"[Scheduler] Found {len(upcoming_appointments)} upcoming appointment(s) for reminder.")

        for appointment in upcoming_appointments:
            if appointment.user and appointment.user.email:
                # Convert UTC → Berlin timezone for email content
                appointment_berlin = appointment.appointment_date.astimezone(BERLIN)

                # Send email reminder
                await send_reminder_email(
                    email=appointment.user.email,
                    title=appointment.title,
                    date=appointment_berlin.strftime("%Y-%m-%d %H:%M"),
                )

                # Mark as sent to prevent duplicate emails
                appointment.reminder_sent = True
                print(f"[Scheduler] Reminder sent for appointment ID {appointment.id} at {appointment_berlin} Berlin time.")

        db.commit()
    except Exception as e:
        print("[Scheduler Error]:", e)
        db.rollback()
    finally:
        db.close()


def start_scheduler():
    """
    Starts the AsyncIOScheduler to run the reminder job every minute.
    For testing, it will look 5 minutes ahead; production should use 60 minutes.
    """
    # Run every minute; test_minutes=5 for quick testing
    scheduler.add_job(check_and_send_reminders, "interval", minutes=1, id="reminder_job", args=[5])
    scheduler.start()
    print("[Scheduler] Started: sending appointment reminders every minute (test mode: 5 mins ahead).")


if __name__ == "__main__":
    start_scheduler()
    asyncio.get_event_loop().run_forever()