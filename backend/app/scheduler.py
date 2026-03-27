# app/scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timedelta, timezone
from app.models import Appointment
from app.database import SessionLocal
from app.email_service import send_reminder_email
import pytz
import asyncio

BERLIN = pytz.timezone("Europe/Berlin")

# 5 for testing → 60 for production)
MINUTES_AHEAD = 60

scheduler = AsyncIOScheduler()


def get_upcoming_appointments(db: Session):
    now_utc = datetime.now(timezone.utc)
    future_limit = now_utc + timedelta(minutes=MINUTES_AHEAD + 1)

    return (
        db.query(Appointment)
        .options(joinedload(Appointment.user))
        .filter(Appointment.reminder_sent == False)
        .filter(Appointment.appointment_date >= now_utc)      # future only
        .filter(Appointment.appointment_date <= future_limit) # within X minutes
        .all()
    )


async def check_and_send_reminders():
    db = SessionLocal()
    try:
        now_utc = datetime.now(timezone.utc)

        appointments = get_upcoming_appointments(db)

        # DEBUG: print ALL appointments in DB
        all_appointments = db.query(Appointment).all()
        print("\n[DEBUG] All appointments in DB:")
        for a in all_appointments:
            print(a.id, a.title, a.appointment_date, a.reminder_sent)
        print("-----\n")

        if not appointments:
            print("[Scheduler] No upcoming appointments.")
            return

        print("[Scheduler] Upcoming appointments:")

        for appt in appointments:
            if not appt.user or not appt.user.email:
                continue

            appt_berlin = appt.appointment_date.astimezone(BERLIN)

            print(f"  → ID={appt.id} | {appt.user.email} | {appt_berlin}")

            try:
                await send_reminder_email(
                    email=appt.user.email,
                    title=appt.title,
                    date=appt_berlin.strftime("%Y-%m-%d %H:%M"),
                )

                appt.reminder_sent = True
                print(f"  Email sent to {appt.user.email}")

            except Exception as e:
                print(f"  Email failed for {appt.user.email}: {e}")

        db.commit()

    except Exception as e:
        print("[Scheduler Error]:", e)
        db.rollback()
    finally:
        db.close()


async def start_scheduler():
    scheduler.add_job(check_and_send_reminders, "interval", minutes=1)
    scheduler.start()
    print(f"[Scheduler] Running every minute (window = {MINUTES_AHEAD} mins)")
    
    while True:
        await asyncio.sleep(10)