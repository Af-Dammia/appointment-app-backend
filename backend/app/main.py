from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <-- import CORS middleware
from app.routers import appointments, auth
from app.database import engine
from app.models import Base

# ✅ Create tables
Base.metadata.create_all(bind=engine)

# ✅ Create app instance
app = FastAPI()

# ✅ Add CORS settings
origins = [
    "http://localhost:3000",  # React default
    "http://localhost:3001",  # Your frontend port
    "https://appointment-app-self.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # allow all origins
    allow_credentials=True,       # allow cookies/auth headers
    allow_methods=["*"],          # GET, POST, DELETE, etc.
    allow_headers=["*"],          # allow all headers
)

# ✅ Include routers AFTER middleware
app.include_router(appointments.router)
app.include_router(auth.router)

# ✅ Test route
@app.get("/")
def home():
    return {"message": "Backend is running"}
from app.email_service import send_reminder_email

@app.get("/test-email")
async def test_email():
    await send_reminder_email(
        "imtiyazansari.1997@gmail.com",  # ⚠️ replace with YOUR email
        "Auslanderbehörde Appointment",
        "Tomorrow 10 AM"
    )
    return {"message": "Email sent"}