"""
Business Logic and Scheduling Services
This module contains the core business logic, including user/volunteer/ride management,
ride matching, and integration with external APIs (mocked Google Maps).
"""
import os
import random
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session # Import Session for database operations
from backend.app import crud, models # Import models for type hinting
from backend.app.models import UserInDB, VolunteerInDB, RideRequestInDB, RideRequestCreate, RideUpdate, RideStatus
from dotenv import load_dotenv

load_dotenv() # Load environment variables

# Mock Google Maps API Key (for demonstration)
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "YOUR_MOCK_GOOGLE_MAPS_API_KEY")

class GoogleMapsService:
    """
    Service to interact with Google Maps API.
    Currently uses mock data. In a real application, this would make
    actual HTTP requests to Google Maps Directions API.
    """
    def get_distance_and_duration(self, origin: str, destination: str) -> Dict[str, float]:
        """
        Mocks a call to Google Maps Directions API to get distance and duration.
        """
        print(f"Mocking Google Maps API call for: {origin} to {destination}")
        # In a real scenario, you'd use requests.get() here
        # For example:
        # import requests
        # url = f"[https://maps.googleapis.com/maps/api/directions/json?origin=](https://maps.googleapis.com/maps/api/directions/json?origin=){origin}&destination={destination}&key={GOOGLE_MAPS_API_KEY}"
        # response = requests.get(url).json()
        # Parse response to get distance_km and duration_minutes

        # Mocked data:
        mock_distance_km = random.uniform(1, 30) # Random distance between 1 and 30 km
        mock_duration_minutes = mock_distance_km * random.uniform(2, 4) # 2-4 minutes per km
        return {"distance_km": round(mock_distance_km, 2), "estimated_duration_minutes": round(mock_duration_minutes, 2)}

class ScheduleManager:
    """
    Manages ride scheduling and volunteer assignment.
    This is where optimization algorithms (Dijkstra, A*) would be integrated
    for more complex routing and scheduling.
    """
    def __init__(self):
        self.google_maps_service = GoogleMapsService()

    async def request_ride(self, db: Session, ride_request_data: RideRequestCreate) -> Optional[models.RideRequest]:
        """
        Handles a new ride request. Calculates distance/duration and saves to DB.
        """
        # Get distance and duration using mock Google Maps API
        route_info = self.google_maps_service.get_distance_and_duration(
            ride_request_data.pickup_address,
            ride_request_data.destination_address
        )

        # Create the ride request in the database
        new_ride_request = crud.create_ride_request(
            db=db,
            ride_request=ride_request_data,
            distance_km=route_info["distance_km"],
            estimated_duration_minutes=route_info["estimated_duration_minutes"]
        )
        return new_ride_request

    async def assign_volunteer_to_ride(self, db: Session, ride_request_id: int, volunteer_id: int) -> Optional[models.RideRequest]:
        """
        Assigns a volunteer to a ride request.
        This is a simple assignment. A real system would have more sophisticated logic.
        """
        ride_request = crud.get_ride_request(db, ride_request_id)
        volunteer = crud.get_volunteer(db, volunteer_id)

        if not ride_request or not volunteer:
            return None # Ride request or volunteer not found

        if ride_request.status != RideStatus.PENDING.value: # Compare with string value from enum
            print(f"Ride request {ride_request_id} is not pending. Cannot assign.")
            return None

        # Update ride request status and assignment details
        update_data = RideUpdate(
            status=RideStatus.ASSIGNED,
            assigned_volunteer_id=volunteer.id,
            assigned_time=datetime.utcnow()
        )
        updated_ride = crud.update_ride_request(db, ride_request_id, update_data)

        # In a more advanced system, you'd update volunteer's schedule/availability here
        print(f"Assigned volunteer {volunteer.name} to ride request {ride_request_id}")
        return updated_ride

    async def complete_ride(self, db: Session, ride_request_id: int) -> Optional[models.RideRequest]:
        """
        Marks a ride as completed.
        """
        ride_request = crud.get_ride_request(db, ride_request_id)
        if not ride_request:
            return None

        if ride_request.status not in [RideStatus.ASSIGNED.value, RideStatus.IN_PROGRESS.value]:
            print(f"Ride request {ride_request_id} is not assigned or in progress. Cannot complete.")
            return None

        update_data = RideUpdate(
            status=RideStatus.COMPLETED,
            completed_time=datetime.utcnow()
        )
        updated_ride = crud.update_ride_request(db, ride_request_id, update_data)
        print(f"Ride request {ride_request_id} marked as completed.")
        return updated_ride

    async def cancel_ride(self, db: Session, ride_request_id: int) -> Optional[models.RideRequest]:
        """
        Marks a ride as cancelled.
        """
        ride_request = crud.get_ride_request(db, ride_request_id)
        if not ride_request:
            return None

        if ride_request.status == RideStatus.COMPLETED.value:
            print(f"Ride request {ride_request_id} is already completed. Cannot cancel.")
            return None

        update_data = RideUpdate(
            status=RideStatus.CANCELLED
        )
        updated_ride = crud.update_ride_request(db, ride_request_id, update_data)
        print(f"Ride request {ride_request_id} marked as cancelled.")
        return updated_ride

    async def find_best_volunteer(self, db: Session, ride_request: models.RideRequest) -> Optional[models.Volunteer]:
        """
        Conceptual function for finding the 'best' volunteer.
        This is where route optimization (Dijkstra/A*) would be used.

        For now, it's a simple greedy approach: find an available volunteer.
        A real implementation would consider:
        - Volunteer's current location vs. pickup_address
        - Volunteer's availability matching requested_time
        - Volunteer's capacity
        - Route efficiency (using Dijkstra/A* on a road network graph)
        - Volunteer preferences
        """
        print(f"Attempting to find best volunteer for ride request {ride_request.id}...")
        available_volunteers = crud.get_volunteers(db) # For simplicity, all are considered 'available'

        # Filter volunteers by availability (conceptual)
        # For example, if ride_request.requested_time is 2025-07-26 10:00:00
        # You'd check if a volunteer's availability list contains a matching slot
        # This requires more sophisticated time slot management.
        # For demonstration, we'll just pick the first available.

        if available_volunteers:
            # In a real scenario, you'd calculate routes for each volunteer
            # and pick the one with the shortest travel time or best fit.
            # Example:
            # for volunteer in available_volunteers:
            #     # Calculate route from volunteer.current_location to ride_request.pickup_address
            #     # Then from pickup_address to destination_address
            #     # Use Dijkstra/A* here if you have a graph representation of roads
            #     pass
            print(f"Found volunteer: {available_volunteers[0].name}")
            return available_volunteers[0]
        print("No suitable volunteer found.")
        return None

    # --- Route Optimization Placeholder ---
    def dijkstra_shortest_path(self, graph, start_node, end_node):
        """
        Placeholder for Dijkstra's algorithm.
        'graph' would represent your road network (e.g., adjacency list/matrix).
        Nodes could be intersections, edges could be road segments with weights (time/distance).
        """
        print(f"Dijkstra's algorithm would calculate shortest path from {start_node} to {end_node}")
        # This would be a full implementation of Dijkstra's algorithm
        # Returns (distance, path)
        return 0, []

    def a_star_shortest_path(self, graph, start_node, end_node, heuristic_function):
        """
        Placeholder for A* algorithm.
        Similar to Dijkstra but uses a heuristic to guide the search,
        making it more efficient for goal-oriented paths.
        """
        print(f"A* algorithm would calculate shortest path from {start_node} to {end_node} with heuristic.")
        # This would be a full implementation of A* algorithm
        # Returns (distance, path)
        return 0, []

# Initialize the ScheduleManager instance
schedule_manager = ScheduleManager()
