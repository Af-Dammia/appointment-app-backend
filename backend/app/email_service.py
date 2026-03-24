from fastapi_mail import FastMail, MessageSchema
from app.email_config import conf

async def send_reminder_email(email: str, title: str, date: str):
    message = MessageSchema(
        subject="Appointment Reminder",
        recipients=[email],
        body=f"Reminder: Your appointment '{title}' is at {date}",
        subtype="plain"
    )

    fm = FastMail(conf)
    await fm.send_message(message)