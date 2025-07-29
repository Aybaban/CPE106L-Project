"""
CRUD Operations for SQLAlchemy Database
This module provides functions for Create, Read, Update, and Delete operations
on the SQLite database tables for Users, Volunteers, and Ride Requests using SQLAlchemy.
"""
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime

# Import SQLAlchemy models and Pydantic schemas
from backend.app import models
from backend.app.models import UserCreate, VolunteerCreate, RideRequestCreate, RideUpdate, RideStatus

# --- User CRUD Operations ---
def create_user(db: Session, user: UserCreate) -> models.User:
    """Creates a new user in the database."""
    db_user = models.User(
        name=user.name,
        phone=user.phone,
        address=user.address,
        user_type=user.user_type.value, # Store enum value as string
        created_at=datetime.utcnow()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    """Retrieves a user by their ID."""
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    """Retrieves all users with pagination."""
    return db.query(models.User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, data: Dict[str, Any]) -> Optional[models.User]:
    """Updates an existing user."""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        for key, value in data.items():
            if key == "user_type":
                setattr(db_user, key, value.value) # Handle enum conversion
            else:
                setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

def delete_user(db: Session, user_id: int) -> bool:
    """Deletes a user by their ID."""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

# --- Volunteer CRUD Operations ---
def create_volunteer(db: Session, volunteer: VolunteerCreate) -> models.Volunteer:
    """Creates a new volunteer in the database."""
    db_volunteer = models.Volunteer(
        name=volunteer.name,
        phone=volunteer.phone,
        car_model=volunteer.car_model,
        license_plate=volunteer.license_plate,
        availability=",".join(volunteer.availability), # Store list as comma-separated string
        current_location=volunteer.current_location,
        created_at=datetime.utcnow()
    )
    db.add(db_volunteer)
    db.commit()
    db.refresh(db_volunteer)
    return db_volunteer

def get_volunteer(db: Session, volunteer_id: int) -> Optional[models.Volunteer]:
    """Retrieves a volunteer by their ID."""
    return db.query(models.Volunteer).filter(models.Volunteer.id == volunteer_id).first()

def get_volunteers(db: Session, skip: int = 0, limit: int = 100) -> List[models.Volunteer]:
    """Retrieves all volunteers with pagination."""
    return db.query(models.Volunteer).offset(skip).limit(limit).all()

def update_volunteer(db: Session, volunteer_id: int, data: Dict[str, Any]) -> Optional[models.Volunteer]:
    """Updates an existing volunteer."""
    db_volunteer = db.query(models.Volunteer).filter(models.Volunteer.id == volunteer_id).first()
    if db_volunteer:
        for key, value in data.items():
            if key == "availability":
                setattr(db_volunteer, key, ",".join(value)) # Convert list to string
            else:
                setattr(db_volunteer, key, value)
        db.commit()
        db.refresh(db_volunteer)
        return db_volunteer
    return None

def delete_volunteer(db: Session, volunteer_id: int) -> bool:
    """Deletes a volunteer by their ID."""
    db_volunteer = db.query(models.Volunteer).filter(models.Volunteer.id == volunteer_id).first()
    if db_volunteer:
        db.delete(db_volunteer)
        db.commit()
        return True
    return False

# --- Ride Request CRUD Operations ---
def create_ride_request(db: Session, ride_request: RideRequestCreate, distance_km: float, estimated_duration_minutes: float) -> models.RideRequest:
    """Creates a new ride request in the database."""
    db_ride_request = models.RideRequest(
        requester_id=ride_request.requester_id,
        pickup_address=ride_request.pickup_address,
        destination_address=ride_request.destination_address,
        requested_time=ride_request.requested_time,
        special_needs=ride_request.special_needs,
        status=RideStatus.PENDING.value, # Default status
        distance_km=distance_km,
        estimated_duration_minutes=estimated_duration_minutes,
        created_at=datetime.utcnow()
    )
    db.add(db_ride_request)
    db.commit()
    db.refresh(db_ride_request)
    return db_ride_request

def get_ride_request(db: Session, ride_request_id: int) -> Optional[models.RideRequest]:
    """Retrieves a ride request by its ID."""
    return db.query(models.RideRequest).filter(models.RideRequest.id == ride_request_id).first()

def get_ride_requests(db: Session, status: Optional[RideStatus] = None, skip: int = 0, limit: int = 100) -> List[models.RideRequest]:
    """Retrieves ride requests, optionally filtered by status, with pagination."""
    query = db.query(models.RideRequest)
    if status:
        query = query.filter(models.RideRequest.status == status.value)
    return query.offset(skip).limit(limit).all()

def update_ride_request(db: Session, ride_request_id: int, data: RideUpdate) -> Optional[models.RideRequest]:
    """Updates an existing ride request."""
    update_data = {k: v for k, v in data.dict(exclude_unset=True).items() if v is not None}
    for key, value in update_data.items():
        if key == "status":
            setattr(db_ride_request, key, value.value) # Handle enum conversion
        else:
            setattr(db_ride_request, key, value)
    db.commit()
    db.refresh(db_ride_request)
    return db_ride_request

def delete_ride_request(db: Session, ride_request_id: int) -> bool:
    """Deletes a ride request by its ID."""
    db_ride_request = db.query(models.RideRequest).filter(models.RideRequest.id == ride_request_id).first()
    if db_ride_request:
        db.delete(db_ride_request)
        db.commit()
        return True
    return False
