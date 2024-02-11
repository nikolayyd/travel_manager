"""
Module containing unit tests for the Trip class.
"""
import unittest
from io import StringIO
from unittest.mock import patch

from src.trips.trip import Trip
from src.utilities.command_handler import add_trip, delete_trip, validate, view_trips
from src.utilities.travel_api import TravelAPI, get_city_code

class TestTrip(unittest.TestCase):
    """Command handler tests."""
    def test_trip_initialization_with_positional_arguments(self):
        """Test for initialization of trip with positional arguments."""
        trip = Trip("New York", "Paris", "2024-03-03", 3500.0, ["travelling"])
        self.assertEqual(trip.start_city, "New York")
        self.assertEqual(trip.destination, "Paris")
        self.assertEqual(trip.date, "2024-03-03")
        self.assertEqual(trip.budget, 3500.0)
        self.assertEqual(trip.activities, ["travelling"])

    def test_trip_initialization_with_keyword_arguments(self):
        """Test for initialization of trip with keyword arguments."""
        trip = Trip(start_city="Sofia", destination="Madrid", date="2024-02-14",
                    budget=1200.0, activities=["riding", "shopping"])
        self.assertEqual(trip.start_city, "Sofia")
        self.assertEqual(trip.destination, "Madrid")
        self.assertEqual(trip.date, "2024-02-14")
        self.assertEqual(trip.budget, 1200.0)
        self.assertEqual(trip.activities, ["riding", "shopping"])

    def test_trip_initialization_with_mixed_arguments(self):
        """Test for initialization of trip with mixed arguments."""
        trip = Trip("Sofia", destination="Paris", date="2024-03-16",
                    budget=2300.0, activities=["swimming", "riding"])
        self.assertEqual(trip.start_city, "Sofia")
        self.assertEqual(trip.destination, "Paris")
        self.assertEqual(trip.date, "2024-03-16")
        self.assertEqual(trip.budget, 2300.0)
        self.assertEqual(trip.activities, ["swimming", "riding"])

    def test_to_dict(self):
        """Test for converting trip object to dictionary."""
        trip = Trip("New York", "Paris", "2024-03-15", 1300.0, ["sightseeing", "shopping"])
        expected_dict = {
            "start_city": "New York",
            "destination": "Paris",
            "date": "2024-03-15",
            "budget": 1300.0,
            "activities": ["sightseeing", "shopping"]
        }
        self.assertEqual(trip.to_dict(), expected_dict)

    def test_from_dict(self):
        """Test for creating trip object from dictionary."""
        trip_data = {
            "start_city": "New York",
            "destination": "Paris",
            "date": "2024-05-15",
            "budget": 1900.0,
            "activities": ["sightseeing", "shopping"]
        }
        trip = Trip.from_dict(trip_data)
        self.assertEqual(trip.start_city, "New York")
        self.assertEqual(trip.destination, "Paris")
        self.assertEqual(trip.date, "2024-05-15")
        self.assertEqual(trip.budget, 1900.0)
        self.assertEqual(trip.activities, ["sightseeing", "shopping"])

class TestCommandHandler(unittest.TestCase):
    """Unit tests for the travel API and other functions in the command handler."""
    def setUp(self):
        self.trips_list = []
        self.api_key = "6cdb45d8bd393c8e04f3e5041e5973de"
        self.travel_api = TravelAPI(self.api_key)

    def test_validate_invalid_date(self):
        """Test for invalid date validation."""
        self.assertFalse(validate("31-12-2022", 1000))

    def test_validate_negative_budget(self):
        """Test for negative budget validation."""
        self.assertFalse(validate("2022-12-31", -100))

    def test_validate_valid_input(self):
        """Test for valid input validation."""
        self.assertTrue(validate("2022-12-31", 1000))

    def test_add_trip(self):
        """Test for adding a trip."""
        with patch('builtins.input',
                   side_effect=["Sofia", "Burgas", "2024-12-10", "1000", "riding, shipping"]):
            add_trip(self.trips_list)
        self.assertEqual(len(self.trips_list), 1)

    def test_view_trips_no_trips(self):
        """Test for viewing trips when no trips are present."""
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            view_trips(self.trips_list)
            self.assertEqual(mock_stdout.getvalue().strip(), "No trips added yet.")

    def test_view_trips_with_trips(self):
        """Test for viewing trips when trips are present."""
        trip = Trip("Burgas", "Madrid", "2024-11-30", 1000, ["swimming", "shopping"])
        self.trips_list.append(trip)
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            view_trips(self.trips_list)
            expected_output = [
                "Trip 1:",
                "Start City: Burgas",
                "Destination: Madrid",
                "Dates: 2024-11-30",
                "Budget: 1000",
                "Activities: swimming, shopping"
            ]
            actual_lines = mock_stdout.getvalue().strip().split("\n")
            for actual_line, expected_line in zip(actual_lines, expected_output):
                self.assertEqual(actual_line.strip(), expected_line.strip())

    def test_delete_trip_invalid_index(self):
        """Test for deleting a trip with invalid index."""
        with patch("sys.stdout", new=StringIO()):
            delete_trip(self.trips_list, -3)
            self.assertEqual(len(self.trips_list), 0)

    def test_delete_trip_valid_index(self):
        """Test for deleting a trip with valid index."""
        trip = Trip("Madrid", "Sofia", "2024-10-15", 1000, ["shopping", "riding"])
        self.trips_list.append(trip)
        with patch("sys.stdout", new=StringIO()):
            delete_trip(self.trips_list, 0) # index - 1
            self.assertEqual(len(self.trips_list), 0)

    def test_travel_api_get_ticket_info(self):
        """Test for getting ticket information from the travel API."""
        ticket_info = self.travel_api.get_ticket_info("Madrid", "London", "2024-03-30")
        self.assertIsInstance(ticket_info, dict)
        self.assertIn("price", ticket_info)
        self.assertIn("departure_at", ticket_info)
        self.assertIn("return_at", ticket_info)
        self.assertIn("expires_at", ticket_info)
        self.assertIn("flight_number", ticket_info)

    def test_get_city_code(self):
        """Test for getting city code."""
        city_code = get_city_code("Sofia")
        self.assertEqual(city_code, "SOF")
        city_code = get_city_code("Madrid")
        self.assertEqual(city_code, "MAD")

unittest.main()
