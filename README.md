# Appointment Reminder App

A full-stack appointment management system with automated email reminders.

## Features

* User Authentication (JWT-based login & signup)
* Create, update, delete appointments
* Automated email reminders before appointments
* Retry mechanism for failed email delivery
* Timezone-safe (stored in UTC, displayed in local time)
* FastAPI backend with async scheduler
* React frontend deployed on Vercel

---

## Tech Stack

### Backend

* FastAPI
* PostgreSQL (Neon DB)
* SQLAlchemy
* APScheduler
* AsyncIO

### Frontend

* React.js
* Axios
* CSS

### Deployment

* Backend: Render
* Frontend: Vercel

---

## How It Works

* Appointments are stored in UTC
* Scheduler runs every minute
* If current time ≥ (appointment time - reminder window)
* Email is sent automatically
* Failed emails are retried up to 3 times

---

## Installation (Backend)

```bash
git clone <https://github.com/Af-Dammia/appointment-app-backend.git>
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## Frontend Setup

```bash
cd frontend
npm install
npm start
```

---

## Demo

### Sign In
<img src = "assets/LoginPage.png" width = "300" />
<img src = "assets/SignIn.png" width = "300" />
<img src = "assets/Sign-InSuccess.png" width = "300" />

### Add Appointment

<img src = "assets/AddAppintment.png", width = "300" />
<img src = "assets/AddAppointmentReset.png", width = "300" />
<img src = "assets/AppontmentUpdatedInList.png", width = "300" />
<img src = "assets/AppointmentTable.png", width = "300" />

### Delete Appointment
<img src = "assets/DeleteAppointment.png", width = "300" />
<img src = "assets/SuccessDelete.png", width = "300" />
<img src = "assets/DeleteAppointmentUpdatedList.png", width = "300" />

### Update Appointment
<img src = "assets/AppointmentUpdate.png", width = "300" />
<img src = "assets/SuccessUpdate.png", width = "300" />
<img src = "assets/DashboardAfterUpdate.png", width = "300" />

### Invalid User or Password
<img src = "assets/UnknownUserLogin.png", width = "300" />
<img src = "assets/UnknownUserLoginFail.png", width = "300" />
<img src = "assets/UserTable.png", width = "300" />

### New User Registration
<img src = "assets/NewUserRegistration.png", width = "300" />
<img src = "assets/RegistrationSuccess.png", width = "300" />
<img src = "assets/DatabaseUpdatedforNewUser.png", width = "300" />

### Console Log for Sendind E-Mail Reminder
<img src = "assets/ConsoleLogOfEmailReminder.png", width = "300" />
<img src = "assets/EmailReceived.png", width = "300" />
<img src = "assets/ReminderSentUpdatedTrue.png", width = "300" />

---

## Future Improvements

* Dashboard with upcoming appointments highlighted
* Real-time notifications
* Mobile responsiveness
* Email templates (HTML styling)
* Role-based access control (admin vs user)
* Background worker system

---

## Author

GitHub: https://github.com/Af-Dammia/ 
