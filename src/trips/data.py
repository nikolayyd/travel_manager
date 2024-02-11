"""
This module provides functions for exporting and importing trip data in JSON format.
"""

import os
import json
from typing import List
from src.trips.trip import Trip

def export_to_json(trips: List[Trip]):
    """
    Exports all the data for the trips in JSON format and save them in the "trips_data.json".
    :param trips: List with objects of class Trip
    """
    trips_data = [trip.to_dict() for trip in trips]

    with open("trips_data.json", "w", encoding="utf-8") as file:
        json.dump(trips_data, file, indent=4)
    print("\nData is exported successfully")

def import_from_json() -> List[Trip]:
    """
    Imports data from the "trips_data.json" file.
    :return: List of Trip objects containing the imported data
    """
    file_path = os.path.join(os.path.dirname(__file__), "trips_data.json")

    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                trips = [Trip.from_dict(trip) for trip in data]
                print("\nData is imported successfully!")
                return trips
        except json.JSONDecodeError:
            print(f"\nError decoding JSON from file '{file_path}'.")
            return []
    else:
        print(f"\nFile '{file_path}' not found.")
        return []
