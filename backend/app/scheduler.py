# app/scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timedelta, timezone
from app.models import Appointment
from app.database import SessionLocal
from app.email_service import send_reminder_email
import pytz
import asyncio

# Berlin timezone
BERLIN = pytz.timezone("Europe/Berlin")

MINUTES_AHEAD = 60

scheduler = AsyncIOScheduler()


def get_pending_appointments(db: Session):
    """
    Get all future appointments where reminder is not sent
    """
    now_utc = datetime.now(timezone.utc)

    return (
        db.query(Appointment)
        .options(joinedload(Appointment.user))
        .filter(Appointment.reminder_sent == False)
        .filter(Appointment.appointment_date >= now_utc)  # only future
        .all()
    )


async def check_and_send_reminders():
    db = SessionLocal()
    try:
        now_utc = datetime.now(timezone.utc)

        appointments = get_pending_appointments(db)
        
        '''
        # DEBUG: print ALL appointments in DB
        all_appointments = db.query(Appointment).all()
        print("\n[DEBUG] All appointments in DB:")
        for a in all_appointments:
            print(a.id, a.title, a.appointment_date, a.reminder_sent)
        print("-----\n")
        '''
        if not appointments:
            print("[Scheduler] No pending appointments.")
            return

        for appt in appointments:
            if not appt.user or not appt.user.email:
                continue

            reminder_time = appt.appointment_date - timedelta(minutes=MINUTES_AHEAD)

            if now_utc >= reminder_time:
                appt_berlin = appt.appointment_date.astimezone(BERLIN)

                print(f"[Scheduler] Sending reminder → ID={appt.id} | {appt.user.email} | {appt_berlin}")

                try:
                    await send_reminder_email(
                        email=appt.user.email,
                        title=appt.title,
                        date=appt_berlin.strftime("%Y-%m-%d %H:%M"),
                    )

                    appt.reminder_sent = True
                    print(f"[Scheduler] Email sent to {appt.user.email}")

                except Exception as e:
                    print(f"[Scheduler] Email failed for {appt.user.email}: {e}")

        db.commit()

    except Exception as e:
        print("[Scheduler Error]:", e)
        db.rollback()
    finally:
        db.close()


async def start_scheduler():
    scheduler.add_job(check_and_send_reminders, "interval", minutes=1)
    scheduler.start()
    print(f"[Scheduler] Started (reminder = {MINUTES_AHEAD} mins before)")

    while True:
        await asyncio.sleep(60)