from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.routers.auth import get_current_user  
from app.database import get_db

router = APIRouter()


# ✅ GET all appointments
@router.get("/appointments", response_model=list[schemas.AppointmentResponse])
def get_appointments(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Appointment).filter(
        models.Appointment.user_id == current_user.id
    ).all()


# ✅ CREATE appointment
@router.post("/appointments", response_model=schemas.AppointmentResponse)
def create_appointment(
    appointment: schemas.AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_appointment = models.Appointment(
        title=appointment.title,
        description=appointment.description,
        appointment_date=appointment.appointment_date,
        user_id=current_user.id
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return new_appointment


# ✅ UPDATE appointment (ONLY ONE VERSION)
@router.put("/appointments/{appointment_id}", response_model=schemas.AppointmentResponse)
def update_appointment(
    appointment_id: int,
    updated_data: schemas.AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    appointment = db.query(models.Appointment).filter(
        models.Appointment.id == appointment_id,
        models.Appointment.user_id == current_user.id
    ).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    # ✅ update all fields
    appointment.title = updated_data.title
    appointment.description = updated_data.description
    appointment.appointment_date = updated_data.appointment_date

    db.commit()
    db.refresh(appointment)

    return appointment


# ✅ DELETE appointment
@router.delete("/appointments/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    appointment = db.query(models.Appointment).filter(
        models.Appointment.id == appointment_id,
        models.Appointment.user_id == current_user.id
    ).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    db.delete(appointment)
    db.commit()

    return {"message": "Appointment deleted successfully"}