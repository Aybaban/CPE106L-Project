import flet as ft
import threading
import time

def main(page: ft.Page):
    page.title = "Ride Scheduler"
    page.window_width = 400
    page.window_height = 500

    def show_start_screen(e=None):
        page.clean()
        page.add(
            ft.Text("Welcome to Ride Scheduler", size=24, weight="bold"),
            ft.Text("Are you a user or a volunteer?", size=16),
            ft.ElevatedButton("I am a User", width=200, on_click=show_user_screen),
            ft.ElevatedButton("I am a Volunteer", width=200, on_click=show_volunteer_screen)
        )

    def show_user_screen(e=None):
        page.clean()
        name_field = ft.TextField(label="Your Name", width=300)
        pickup_field = ft.TextField(label="Pickup Address", width=300)
        dest_field = ft.TextField(label="Destination", width=300)
        time_field = ft.TextField(label="Time (e.g., 02:30 PM)", width=300, hint_text="e.g., 02:30 PM")
        date_field = ft.TextField(label="Date (YYYY-MM-DD, optional)", width=300, hint_text="e.g., 2024-07-01")

        def request_ride(e):
            show_searching_screen()

        page.add(
            ft.Text("Request a Ride", size=24, weight="bold"),
            name_field,
            pickup_field,
            dest_field,
            time_field,
            date_field,
            ft.ElevatedButton("Request Ride", width=200, on_click=request_ride),
            ft.ElevatedButton("Back", width=200, on_click=show_start_screen)
        )

    def show_arrival_screen():
        page.clean()
        page.add(
            ft.Text("Volunteer Assigned!", size=24, weight="bold"),
            ft.Text("Your volunteer will arrive at approximately 02:45 PM.", size=18),
            ft.ElevatedButton("Back to Home", width=200, on_click=show_start_screen)
        )

    searching_cancelled = {"value": False}

    def show_searching_screen():
        searching_cancelled["value"] = False
        page.clean()
        searching_text = ft.Text("Looking for a volunteer...", size=20, weight="bold")
        cancel_btn = ft.ElevatedButton("Cancel Request", width=200)
        progress = ft.ProgressRing()
        page.add(searching_text, progress, cancel_btn)

        def cancel_search(e):
            searching_cancelled["value"] = True
            show_user_screen()

        cancel_btn.on_click = cancel_search

        def simulate_volunteer_search():
            time.sleep(2)
            if not searching_cancelled["value"]:
                page.dialog = ft.AlertDialog(
                    title=ft.Text("Volunteer Found!"),
                    content=ft.Text("A volunteer has been found for your ride."),
                    open=True
                )
                page.update()
                time.sleep(3)
                if not searching_cancelled["value"]:
                    page.dialog.open = False
                    page.update()
                    show_arrival_screen()

        threading.Thread(target=simulate_volunteer_search, daemon=True).start()

    def show_volunteer_screen(e=None):
        page.clean()
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day_checks = [ft.Checkbox(label=day) for day in days]
        start_time = ft.TextField(label="Start Time (HH:MM)", width=140)
        end_time = ft.TextField(label="End Time (HH:MM)", width=140)

        def save_availability(e):
            selected_days = [cb.label for cb in day_checks if cb.value]
            page.dialog = ft.AlertDialog(
                title=ft.Text("Availability Saved"),
                content=ft.Text(f"Availability saved for {', '.join(selected_days)} from {start_time.value} to {end_time.value}"),
                open=True
            )
            page.update()

        page.add(
            ft.Text("Volunteer Availability", size=24, weight="bold"),
            ft.Text("Select your available days:", size=16),
            ft.Column(day_checks, spacing=5),
            ft.Row([start_time, end_time], spacing=10),
            ft.ElevatedButton("Save Availability", width=200, on_click=save_availability),
            ft.ElevatedButton("Back", width=200, on_click=show_start_screen)
        )

    show_start_screen()

ft.app(target=main)