
"""
FastAPI Application Entry Point
This module sets up the FastAPI application, defines API routes,
and handles dependency injection for database and services.
"""
from fastapi import FastAPI, HTTPException, Depends, status
from typing import List, Optional
from datetime import datetime
from backend.app import crud
from backend.app.models import UserCreate, UserInDB, VolunteerCreate, VolunteerInDB, RideRequestCreate, RideRequestInDB, RideAssignment, RideUpdate, RideStatus, PyObjectId
from backend.app.services import schedule_manager
from backend.app.database import connect_to_mongo, client as mongo_client # Import client to close it on shutdown

app = FastAPI(
    title="Ride Scheduling API",
    description="API for managing ride requests, volunteers, and users for accessibility needs.",
    version="1.0.0"
)

# --- Event Handlers for Application Startup/Shutdown ---
@app.on_event("startup")
async def startup_db_client():
    """Connect to MongoDB on application startup."""
    connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    """Close MongoDB connection on application shutdown."""
    if mongo_client:
        mongo_client.close()
        print("MongoDB connection closed.")

# --- API Routes ---

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Ride Scheduling API!"}

# --- User Endpoints ---
@app.post("/users/", response_model=UserInDB, status_code=status.HTTP_201_CREATED, tags=["Users"])
async def create_new_user(user: UserCreate):
    """Create a new user."""
    return await crud.create_user(user)

@app.get("/users/", response_model=List[UserInDB], tags=["Users"])
async def read_users():
    """Retrieve all users."""
    return await crud.get_users()

@app.get("/users/{user_id}", response_model=UserInDB, tags=["Users"])
async def read_user(user_id: str):
    """Retrieve a single user by ID."""
    user = await crud.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=UserInDB, tags=["Users"])
async def update_existing_user(user_id: str, user_data: UserCreate): # Using UserCreate for update data
    """Update an existing user."""
    updated_user = await crud.update_user(user_id, user_data.dict(exclude_unset=True))
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found or no changes made")
    return updated_user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
async def delete_existing_user(user_id: str):
    """Delete a user by ID."""
    if not await crud.delete_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return

# --- Volunteer Endpoints ---
@app.post("/volunteers/", response_model=VolunteerInDB, status_code=status.HTTP_201_CREATED, tags=["Volunteers"])
async def create_new_volunteer(volunteer: VolunteerCreate):
    """Create a new volunteer."""
    return await crud.create_volunteer(volunteer)

@app.get("/volunteers/", response_model=List[VolunteerInDB], tags=["Volunteers"])
async def read_volunteers():
    """Retrieve all volunteers."""
    return await crud.get_volunteers()

@app.get("/volunteers/{volunteer_id}", response_model=VolunteerInDB, tags=["Volunteers"])
async def read_volunteer(volunteer_id: str):
    """Retrieve a single volunteer by ID."""
    volunteer = await crud.get_volunteer(volunteer_id)
    if volunteer is None:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    return volunteer

@app.put("/volunteers/{volunteer_id}", response_model=VolunteerInDB, tags=["Volunteers"])
async def update_existing_volunteer(volunteer_id: str, volunteer_data: VolunteerCreate): # Using VolunteerCreate for update data
    """Update an existing volunteer."""
    updated_volunteer = await crud.update_volunteer(volunteer_id, volunteer_data.dict(exclude_unset=True))
    if updated_volunteer is None:
        raise HTTPException(status_code=404, detail="Volunteer not found or no changes made")
    return updated_volunteer

@app.delete("/volunteers/{volunteer_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Volunteers"])
async def delete_existing_volunteer(volunteer_id: str):
    """Delete a volunteer by ID."""
    if not await crud.delete_volunteer(volunteer_id):
        raise HTTPException(status_code=404, detail="Volunteer not found")
    return

# --- Ride Request Endpoints ---
@app.post("/rides/", response_model=RideRequestInDB, status_code=status.HTTP_201_CREATED, tags=["Rides"])
async def request_new_ride(ride_request: RideRequestCreate):
    """
    Request a new ride.
    The system will calculate distance/duration and save the request.
    """
    # Validate requester_id exists
    requester = await crud.get_user(str(ride_request.requester_id))
    if not requester:
        raise HTTPException(status_code=400, detail="Requester user not found.")

    new_ride = await schedule_manager.request_ride(ride_request)
    return new_ride

@app.get("/rides/", response_model=List[RideRequestInDB], tags=["Rides"])
async def get_all_ride_requests(status: Optional[RideStatus] = None):
    """Retrieve all ride requests, optionally filtered by status."""
    return await crud.get_ride_requests(status=status)

@app.get("/rides/{ride_id}", response_model=RideRequestInDB, tags=["Rides"])
async def get_ride_request_by_id(ride_id: str):
    """Retrieve a single ride request by ID."""
    ride = await crud.get_ride_request(ride_id)
    if ride is None:
        raise HTTPException(status_code=404, detail="Ride request not found")
    return ride

@app.post("/rides/{ride_id}/assign", response_model=RideRequestInDB, tags=["Rides"])
async def assign_volunteer_to_ride_request(ride_id: str, assignment: RideAssignment):
    """Assign a volunteer to a specific ride request."""
    if str(assignment.ride_request_id) != ride_id:
        raise HTTPException(status_code=400, detail="Ride ID in path and body do not match.")

    assigned_ride = await schedule_manager.assign_volunteer_to_ride(ride_id, str(assignment.volunteer_id))
    if assigned_ride is None:
        raise HTTPException(status_code=400, detail="Failed to assign volunteer. Ride or volunteer not found, or ride not pending.")
    return assigned_ride

@app.post("/rides/{ride_id}/complete", response_model=RideRequestInDB, tags=["Rides"])
async def complete_ride_request(ride_id: str):
    """Mark a ride request as completed."""
    completed_ride = await schedule_manager.complete_ride(ride_id)
    if completed_ride is None:
        raise HTTPException(status_code=400, detail="Failed to complete ride. Ride not found or not in assignable/in-progress status.")
    return completed_ride

@app.post("/rides/{ride_id}/cancel", response_model=RideRequestInDB, tags=["Rides"])
async def cancel_ride_request(ride_id: str):
    """Mark a ride request as cancelled."""
    cancelled_ride = await schedule_manager.cancel_ride(ride_id)
    if cancelled_ride is None:
        raise HTTPException(status_code=400, detail="Failed to cancel ride. Ride not found or already completed.")
    return cancelled_ride

@app.put("/rides/{ride_id}", response_model=RideRequestInDB, tags=["Rides"])
async def update_ride_request_details(ride_id: str, ride_update: RideUpdate):
    """Update details of a ride request (e.g., status, assigned volunteer)."""
    updated_ride = await crud.update_ride_request(ride_id, ride_update)
    if updated_ride is None:
        raise HTTPException(status_code=404, detail="Ride request not found or no changes made.")
    return updated_ride

@app.delete("/rides/{ride_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"]) # Changed tag from "Rides" to "Users"
async def delete_ride_request_by_id(ride_id: str):
    """Delete a ride request by ID."""
    if not await crud.delete_ride_request(ride_id):
        raise HTTPException(status_code=404, detail="Ride request not found")
    return
