"""
Module containing the Trip class for representing travel trips.
"""
from typing import List, Dict, Any

class Trip:
    """Represents a trip with specific destination, trip date, budget, and activities."""
    def __init__(self, *args, **kwargs):
        """
        Initializes a new trip with specific start city,
        destination, trip date, budget and activities.
        :param start_city: Trip starting city
        :param destination: Trip destination
        :param date: Trip date
        :param budget: Budget for the trip
        :param activities: List of activities for the trip
        """
        self.start_city: str = kwargs.get("start_city", args[0] if args else "")
        self.destination: str = kwargs.get("destination", args[1] if len(args) > 1 else "")
        self.date: str = kwargs.get("date", args[2] if len(args) > 2 else "")
        self.budget: float = kwargs.get("budget", args[3] if len(args) > 3 else 0.0)
        self.activities: List[str] = kwargs.get("activities", args[4] if len(args) > 4 else [])

    def to_dict(self) -> Dict[str, Any]:
        """
        Returns the object as a dict.
        """
        return {
            "start_city": self.start_city,
            "destination": self.destination,
            "date": self.date,
            "budget": self.budget,
            "activities": self.activities,
        }

    @staticmethod
    def from_dict(trip_data: Dict[str, Any]) -> "Trip":
        """
        Create an object of type Trip from a dict.

        :param trip_data: Dict with data for the trip
        :return: object Trip
        """
        trip = Trip(
            trip_data["start_city"],
            trip_data["destination"],
            trip_data["date"],
            trip_data["budget"],
            trip_data["activities"]
        )
        return trip
