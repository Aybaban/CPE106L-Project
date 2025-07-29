"""
Pydantic Models for API Request/Response and Data Structures
This module defines the data models used throughout the application,
leveraging Pydantic for data validation and serialization.
"""
from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator # NEW IMPORT
from typing import List, Optional, Any, Annotated # MODIFIED IMPORT (added Annotated, Any)
from datetime import datetime
from enum import Enum

# Custom ObjectId type for MongoDB
from bson import ObjectId

# Validator function for ObjectId
def validate_objectid(value: Any) -> ObjectId:
    if isinstance(value, ObjectId):
        return value
    if isinstance(value, str):
        if ObjectId.is_valid(value):
            return ObjectId(value)
    raise ValueError("Invalid ObjectId")

# Define PyObjectId as an Annotated type for Pydantic v2
PyObjectId = Annotated[ObjectId, BeforeValidator(validate_objectid)]


class UserType(str, Enum):
    ELDERLY = "elderly"
    ACCESSIBILITY = "accessibility"

class RideStatus(str, Enum):
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
    id: PyObjectId = Field(default_factory=lambda: ObjectId(), alias="_id") # Updated default_factory
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class VolunteerBase(BaseModel):
    name: str
    phone: str
    car_model: Optional[str] = None
    license_plate: Optional[str] = None
    availability: List[str] = Field(default_factory=list) # e.g., ["Monday 9-12", "Wednesday 1-4"]
    current_location: Optional[str] = None # For real-time location tracking (conceptual)

class VolunteerCreate(VolunteerBase):
    pass

class VolunteerInDB(VolunteerBase):
    id: PyObjectId = Field(default_factory=lambda: ObjectId(), alias="_id") # Updated default_factory
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class RideRequestBase(BaseModel):
    requester_id: PyObjectId # Changed to PyObjectId
    pickup_address: str
    destination_address: str
    requested_time: datetime
    special_needs: Optional[str] = None

class RideRequestCreate(RideRequestBase):
    pass

class RideRequestInDB(RideRequestBase):
    id: PyObjectId = Field(default_factory=lambda: ObjectId(), alias="_id") # Updated default_factory
    status: RideStatus = RideStatus.PENDING
    assigned_volunteer_id: Optional[PyObjectId] = None # Changed to PyObjectId
    assigned_time: Optional[datetime] = None
    completed_time: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    distance_km: Optional[float] = None # Calculated from Google Maps API
    estimated_duration_minutes: Optional[float] = None # Calculated from Google Maps API

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class RideAssignment(BaseModel):
    ride_request_id: PyObjectId # Changed to PyObjectId
    volunteer_id: PyObjectId # Changed to PyObjectId

class RideUpdate(BaseModel):
    status: Optional[RideStatus] = None
    assigned_volunteer_id: Optional[PyObjectId] = None # Changed to PyObjectId
    assigned_time: Optional[datetime] = None
    completed_time: Optional[datetime] = None
