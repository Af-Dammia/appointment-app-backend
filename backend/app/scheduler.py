# app/scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.email_service import send_reminder_email
from app.database import get_upcoming_appointments 

scheduler = AsyncIOScheduler()

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