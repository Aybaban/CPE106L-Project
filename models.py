"""
Models for Database Tables and Pydantic Models for API Request/Response
This module defines the SQLAlchemy ORM models that map to database tables,
and Pydantic models for data validation and serialization in the API.
"""
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum # Use an alias to avoid conflict with SQLAlchemy's Enum
from pydantic import BaseModel, Field
from typing import List, Optional

# Import the Base from database.py to define SQLAlchemy models
from backend.app.database import Base

# --- SQLAlchemy ORM Models (Database Tables) ---

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone = Column(String, unique=True, index=True)
    address = Column(String)
    user_type = Column(Enum('elderly', 'accessibility', name='user_type_enum'), default='elderly')
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to RideRequest (one-to-many)
    ride_requests = relationship("RideRequest", back_populates="requester")

class Volunteer(Base):
    __tablename__ = "volunteers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone = Column(String, unique=True, index=True)
    car_model = Column(String, nullable=True)
    license_plate = Column(String, nullable=True)
    # Storing availability as a comma-separated string for simplicity
    # For complex scheduling, a separate Availability table would be better
    availability = Column(String, default="") # e.g., "Monday 9-12,Wednesday 1-4"
    current_location = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to RideRequest (one-to-many)
    assigned_rides = relationship("RideRequest", back_populates="assigned_volunteer")

class RideRequest(Base):
    __tablename__ = "ride_requests"

    id = Column(Integer, primary_key=True, index=True)
    requester_id = Column(Integer, ForeignKey("users.id"))
    pickup_address = Column(String)
    destination_address = Column(String)
    requested_time = Column(DateTime)
    special_needs = Column(String, nullable=True)
    status = Column(Enum('pending', 'assigned', 'in_progress', 'completed', 'cancelled', name='ride_status_enum'), default='pending')
    assigned_volunteer_id = Column(Integer, ForeignKey("volunteers.id"), nullable=True)
    assigned_time = Column(DateTime, nullable=True)
    completed_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    distance_km = Column(Float, nullable=True)
    estimated_duration_minutes = Column(Float, nullable=True)

    # Relationships
    requester = relationship("User", back_populates="ride_requests")
    assigned_volunteer = relationship("Volunteer", back_populates="assigned_rides")


# --- Pydantic Models (API Request/Response Schemas) ---

class UserType(str, PyEnum): # Using PyEnum for Pydantic
    ELDERLY = "elderly"
    ACCESSIBILITY = "accessibility"

class RideStatus(str, PyEnum): # Using PyEnum for Pydantic
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class UserBase(BaseModel):
    name: str
    phone: str
    address: str
    user_type: UserType

class UserCreate(UserBase):
    pass

class UserInDB(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True # Enable ORM mode for Pydantic to read from SQLAlchemy models

class VolunteerBase(BaseModel):
    name: str
    phone: str
    car_model: Optional[str] = None
    license_plate: Optional[str] = None
    availability: List[str] = Field(default_factory=list) # e.g., ["Monday 9-12", "Wednesday 1-4"]
    current_location: Optional[str] = None

class VolunteerCreate(VolunteerBase):
    pass

class VolunteerInDB(VolunteerBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class RideRequestBase(BaseModel):
    requester_id: int
    pickup_address: str
    destination_address: str
    requested_time: datetime
    special_needs: Optional[str] = None

class RideRequestCreate(RideRequestBase):
    pass

class RideRequestInDB(RideRequestBase):
    id: int
    status: RideStatus = RideStatus.PENDING
    assigned_volunteer_id: Optional[int] = None
    assigned_time: Optional[datetime] = None
    completed_time: Optional[datetime] = None
    created_at: datetime
    distance_km: Optional[float] = None
    estimated_duration_minutes: Optional[float] = None

    class Config:
        orm_mode = True

class RideAssignment(BaseModel):
    ride_request_id: int
    volunteer_id: int

class RideUpdate(BaseModel):
    status: Optional[RideStatus] = None
    assigned_volunteer_id: Optional[int] = None
    assigned_time: Optional[datetime] = None
    completed_time: Optional[datetime] = None
