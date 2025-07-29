"""
Flet Desktop Application for Ride Scheduling
This application provides a simple UI for users to request rides
and for administrators/volunteers to view ride requests.
It interacts with the FastAPI backend.
"""
import flet as ft
import requests
import json
from datetime import datetime

# Base URL for the FastAPI backend
API_BASE_URL = "http://localhost:8000" # Ensure this matches your FastAPI server's address and port

class RideApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Community Ride Scheduler"
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.window_width = 800
        self.page.window_height = 700
        self.page.theme_mode = ft.ThemeMode.LIGHT # Or DARK

        # Initialize UI elements
        # Changed requester_id_input to expect integer for SQL
        self.requester_id_input = ft.TextField(label="Your User ID (e.g., 1, 2)", width=300, input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]", replacement_string=""))
        self.pickup_address_input = ft.TextField(label="Pickup Address", width=300)
        self.destination_address_input = ft.TextField(label="Destination Address", width=300)
        self.requested_time_input = ft.TextField(label="Requested Time (YYYY-MM-DD HH:MM)", width=300)
        self.special_needs_input = ft.TextField(label="Special Needs (Optional)", multiline=True, min_lines=2, max_lines=4, width=300)
        self.request_ride_button = ft.ElevatedButton("Request Ride", on_click=self.request_ride, icon=ft.icons.CAR_CRASH)

        self.message_text = ft.Text("", color=ft.colors.BLUE_700, size=16)

        self.ride_requests_view = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)

        self.page.add(
            ft.AppBar(
                title=ft.Text("Community Ride Scheduler", color=ft.colors.WHITE),
                bgcolor=ft.colors.BLUE_700,
                center_title=True,
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Request a New Ride", size=24, weight=ft.FontWeight.BOLD),
                        self.requester_id_input,
                        self.pickup_address_input,
                        self.destination_address_input,
                        self.requested_time_input,
                        self.special_needs_input,
                        self.request_ride_button,
                        self.message_text,
                        ft.Divider(),
                        ft.Text("Current Ride Requests", size=24, weight=ft.FontWeight.BOLD),
                        ft.ElevatedButton("Refresh Rides", on_click=self.refresh_ride_requests, icon=ft.icons.REFRESH),
                        self.ride_requests_view,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                ),
                padding=20,
                margin=20,
                border_radius=ft.border_radius.all(10),
                bgcolor=ft.colors.WHITE,
                shadow=ft.BoxShadow(
                    spread_radius=2,
                    blur_radius=10,
                    color=ft.colors.BLACK_26,
                    offset=ft.Offset(0, 0),
                ),
                width=600,
                alignment=ft.alignment.center,
            )
        )
        self.refresh_ride_requests() # Load rides on startup

    async def request_ride(self, e):
        """Handles the ride request submission."""
        self.message_text.value = "Requesting ride..."
        self.message_text.color = ft.colors.BLUE_700
        self.page.update()

        requester_id_str = self.requester_id_input.value
        pickup_address = self.pickup_address_input.value
        destination_address = self.destination_address_input.value
        requested_time_str = self.requested_time_input.value
        special_needs = self.special_needs_input.value

        if not all([requester_id_str, pickup_address, destination_address, requested_time_str]):
            self.message_text.value = "Please fill in all required fields."
            self.message_text.color = ft.colors.RED_500
            self.page.update()
            return

        try:
            requester_id = int(requester_id_str) # Convert to int for SQL backend
        except ValueError:
            self.message_text.value = "User ID must be an integer."
            self.message_text.color = ft.colors.RED_500
            self.page.update()
            return

        try:
            # Convert string to datetime object
            requested_time_dt = datetime.strptime(requested_time_str, "%Y-%m-%d %H:%M")
        except ValueError:
            self.message_text.value = "Invalid time format. Use YYYY-MM-DD HH:MM"
            self.message_text.color = ft.colors.RED_500
            self.page.update()
            return

        ride_data = {
            "requester_id": requester_id,
            "pickup_address": pickup_address,
            "destination_address": destination_address,
            "requested_time": requested_time_dt.isoformat() + "Z", # ISO 8601 format with Z for UTC
            "special_needs": special_needs if special_needs else None,
        }

        try:
            response = requests.post(f"{API_BASE_URL}/rides/", json=ride_data)
            response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
            new_ride = response.json()
            self.message_text.value = f"Ride requested successfully! ID: {new_ride['id']}"
            self.message_text.color = ft.colors.GREEN_500
            # Clear input fields
            self.pickup_address_input.value = ""
            self.destination_address_input.value = ""
            self.requested_time_input.value = ""
            self.special_needs_input.value = ""
            await self.refresh_ride_requests(e) # Refresh the list of rides
        except requests.exceptions.RequestException as e:
            self.message_text.value = f"Error requesting ride: {e}"
            self.message_text.color = ft.colors.RED_500
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json().get("detail", "Unknown error")
                    self.message_text.value += f" (Detail: {error_detail})"
                except json.JSONDecodeError:
                    self.message_text.value += f" (Response: {e.response.text})"
        except Exception as e:
            self.message_text.value = f"An unexpected error occurred: {e}"
            self.message_text.color = ft.colors.RED_500
        finally:
            self.page.update()

    async def refresh_ride_requests(self, e):
        """Fetches and displays current ride requests."""
        self.ride_requests_view.controls.clear()
        self.ride_requests_view.controls.append(ft.ProgressRing(width=20, height=20))
        self.page.update()

        try:
            response = requests.get(f"{API_BASE_URL}/rides/")
            response.raise_for_status()
            rides = response.json()

            self.ride_requests_view.controls.clear()
            if not rides:
                self.ride_requests_view.controls.append(ft.Text("No ride requests found.", italic=True))
            else:
                for ride in rides:
                    # Format requested_time
                    try:
                        req_time = datetime.fromisoformat(ride['requested_time'].replace('Z', '+00:00')).strftime("%Y-%m-%d %H:%M")
                    except ValueError:
                        req_time = ride['requested_time'] # Fallback if parsing fails

                    self.ride_requests_view.controls.append(
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text(f"Ride ID: {ride['id']}", size=14, weight=ft.FontWeight.BOLD),
                                        ft.Text(f"From: {ride['pickup_address']}", size=12),
                                        ft.Text(f"To: {ride['destination_address']}", size=12),
                                        ft.Text(f"Requested: {req_time}", size=12),
                                        ft.Text(f"Status: {ride['status'].upper()}", size=12, color=self.get_status_color(ride['status'])),
                                        ft.Text(f"Distance: {ride.get('distance_km', 'N/A')} km", size=12),
                                        ft.Text(f"Est. Duration: {ride.get('estimated_duration_minutes', 'N/A')} min", size=12),
                                        ft.Text(f"Special Needs: {ride.get('special_needs', 'None')}", size=12, italic=True),
                                        ft.Row(
                                            [
                                                ft.ElevatedButton(
                                                    "Assign Volunteer (Mock)",
                                                    on_click=lambda _, ride_id=ride['id']: self.assign_mock_volunteer(ride_id),
                                                    disabled=(ride['status'] != 'pending'),
                                                    icon=ft.icons.PERSON_ADD
                                                ),
                                                ft.ElevatedButton(
                                                    "Complete Ride",
                                                    on_click=lambda _, ride_id=ride['id']: self.complete_ride(ride_id),
                                                    disabled=(ride['status'] != 'assigned' and ride['status'] != 'in_progress'),
                                                    icon=ft.icons.CHECK_CIRCLE_OUTLINE
                                                ),
                                                ft.ElevatedButton(
                                                    "Cancel Ride",
                                                    on_click=lambda _, ride_id=ride['id']: self.cancel_ride(ride_id),
                                                    disabled=(ride['status'] == 'completed' or ride['status'] == 'cancelled'),
                                                    icon=ft.icons.CANCEL
                                                ),
                                            ],
                                            spacing=10,
                                            wrap=True
                                        )
                                    ],
                                    spacing=5,
                                ),
                                padding=15,
                            ),
                            width=550,
                            elevation=3,
                        )
                    )
        except requests.exceptions.RequestException as e:
            self.ride_requests_view.controls.clear()
            self.ride_requests_view.controls.append(ft.Text(f"Error fetching rides: {e}", color=ft.colors.RED_500))
        finally:
            self.page.update()

    def get_status_color(self, status: str):
        """Returns a color based on ride status."""
        if status == 'pending':
            return ft.colors.ORANGE_500
        elif status == 'assigned':
            return ft.colors.BLUE_500
        elif status == 'in_progress':
            return ft.colors.CYAN_500
        elif status == 'completed':
            return ft.colors.GREEN_500
        elif status == 'cancelled':
            return ft.colors.RED_500
        return ft.colors.BLACK

    async def assign_mock_volunteer(self, ride_id: int): # Changed ride_id type hint to int
        """Mocks assigning a volunteer to a ride."""
        self.message_text.value = f"Assigning mock volunteer to ride {ride_id}..."
        self.message_text.color = ft.colors.BLUE_700
        self.page.update()

        # First, ensure there's at least one volunteer to assign
        try:
            volunteers_response = requests.get(f"{API_BASE_URL}/volunteers/")
            volunteers_response.raise_for_status()
            volunteers = volunteers_response.json()
            if not volunteers:
                self.message_text.value = "No volunteers available to assign. Please add a volunteer first."
                self.message_text.color = ft.colors.RED_500
                self.page.update()
                return

            # Pick the first volunteer for simplicity
            mock_volunteer_id = volunteers[0]['id'] # This will be an integer from SQL

            assignment_data = {
                "ride_request_id": ride_id,
                "volunteer_id": mock_volunteer_id
            }
            # Ensure ride_id is passed as int in URL for SQL backend
            response = requests.post(f"{API_BASE_URL}/rides/{ride_id}/assign", json=assignment_data)
            response.raise_for_status()
            self.message_text.value = f"Ride {ride_id} assigned to volunteer {volunteers[0]['name']}!"
            self.message_text.color = ft.colors.GREEN_500
            await self.refresh_ride_requests(None)
        except requests.exceptions.RequestException as e:
            self.message_text.value = f"Error assigning volunteer: {e}"
            self.message_text.color = ft.colors.RED_500
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json().get("detail", "Unknown error")
                    self.message_text.value += f" (Detail: {error_detail})"
                except json.JSONDecodeError:
                    self.message_text.value += f" (Response: {e.response.text})"
        finally:
            self.page.update()

    async def complete_ride(self, ride_id: int): # Changed ride_id type hint to int
        """Marks a ride as completed."""
        self.message_text.value = f"Completing ride {ride_id}..."
        self.message_text.color = ft.colors.BLUE_700
        self.page.update()
        try:
            response = requests.post(f"{API_BASE_URL}/rides/{ride_id}/complete") # Ensure ride_id is passed as int in URL
            response.raise_for_status()
            self.message_text.value = f"Ride {ride_id} marked as completed!"
            self.message_text.color = ft.colors.GREEN_500
            await self.refresh_ride_requests(None)
        except requests.exceptions.RequestException as e:
            self.message_text.value = f"Error completing ride: {e}"
            self.message_text.color = ft.colors.RED_500
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json().get("detail", "Unknown error")
                    self.message_text.value += f" (Detail: {error_detail})"
                except json.JSONDecodeError:
                    self.message_text.value += f" (Response: {e.response.text})"
        finally:
            self.page.update()

    async def cancel_ride(self, ride_id: int): # Changed ride_id type hint to int
        """Marks a ride as cancelled."""
        self.message_text.value = f"Cancelling ride {ride_id}..."
        self.message_text.color = ft.colors.BLUE_700
        self.page.update()
        try:
            response = requests.post(f"{API_BASE_URL}/rides/{ride_id}/cancel") # Ensure ride_id is passed as int in URL
            response.raise_for_status()
            self.message_text.value = f"Ride {ride_id} marked as cancelled!"
            self.message_text.color = ft.colors.GREEN_500
            await self.refresh_ride_requests(None)
        except requests.exceptions.RequestException as e:
            self.message_text.value = f"Error cancelling ride: {e}"
            self.message_text.color = ft.colors.RED_500
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json().get("detail", "Unknown error")
                    self.message_text.value += f" (Detail: {error_detail})"
                except json.JSONDecodeError:
                    self.message_text.value += f" (Response: {e.response.text})"
        finally:
            self.page.update()

def main(page: ft.Page):
    RideApp(page)

if __name__ == "__main__":
    ft.app(target=main)

```text
# frontend/requirements.txt
flet==0.23.0
requests==2.32.3
