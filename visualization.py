"""
Matplotlib Visualization Utilities
This module provides functions to visualize ride data,
such as ride frequency over time or wait times.
"""
import matplotlib.pyplot as plt
import requests
from datetime import datetime
from collections import Counter

# Base URL for the FastAPI backend
API_BASE_URL = "http://localhost:8000"

def plot_ride_frequency_by_day():
    """
    Fetches all ride requests and plots their frequency by day.
    """
    try:
        response = requests.get(f"{API_BASE_URL}/rides/")
        response.raise_for_status()
        rides = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching rides from API: {e}")
        return

    if not rides:
        print("No ride data available for visualization.")
        return

    # Extract dates from requested_time
    dates = []
    for ride in rides:
        try:
            # Handle ISO 8601 format with or without 'Z'
            dt_object = datetime.fromisoformat(ride['requested_time'].replace('Z', '+00:00'))
            dates.append(dt_object.date())
        except ValueError:
            print(f"Warning: Could not parse date for ride {ride.get('id', 'N/A')}: {ride['requested_time']}")
            continue

    if not dates:
        print("No valid dates found in ride data.")
        return

    # Count frequency of each date
    date_counts = Counter(dates)

    # Sort dates for plotting
    sorted_dates = sorted(date_counts.keys())
    frequencies = [date_counts[d] for d in sorted_dates]

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.bar([str(d) for d in sorted_dates], frequencies, color='skyblue')
    plt.xlabel("Date")
    plt.ylabel("Number of Rides")
    plt.title("Ride Request Frequency by Day")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def plot_ride_status_distribution():
    """
    Fetches all ride requests and plots the distribution of their statuses.
    """
    try:
        response = requests.get(f"{API_BASE_URL}/rides/")
        response.raise_for_status()
        rides = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching rides from API: {e}")
        return

    if not rides:
        print("No ride data available for visualization.")
        return

    status_counts = Counter(ride['status'] for ride in rides)

    labels = status_counts.keys()
    sizes = status_counts.values()
    colors = ['gold', 'lightcoral', 'lightskyblue', 'lightgreen', 'silver']

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title("Ride Request Status Distribution")
    plt.show()

if __name__ == "__main__":
    print("Generating ride frequency plot...")
    plot_ride_frequency_by_day()
    print("\nGenerating ride status distribution plot...")
    plot_ride_status_distribution()

```text
# utils/requirements.txt
matplotlib==3.9.0
requests==2.32.3
