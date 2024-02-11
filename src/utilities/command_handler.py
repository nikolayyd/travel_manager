"""
Module containing functions for handling user commands related to trips and travel information.
"""

from typing import List, Tuple, Union
from datetime import datetime
from src.trips.trip import Trip
from src.trips.data import import_from_json, export_to_json
from src.utilities.travel_api import TravelAPI

def validate(date: str, budget: float) -> bool:
    """
    Validate the date format as dd-mm-yyyy and check if the budget is positive.

    :param date: A string representing the date to be validated
    :param budget: The budget to be validated
    :return: True if the date and budget are valid, False otherwise
    """
    try:
        datetime.strptime(date, "%Y-%m-%d")
        if budget <= 0:
            return False
        return True
    except ValueError:
        return False

def add_trip(trip_list: List[Trip]):
    """
    Adds a new trip to the trip list.

    :param trip_list: List of Trip objects to add the new trip to
    """
    start_city = input("\nEnter start city: ")
    destination = input("\nEnter destination: ")
    date = input("\nEnter date: ")
    budget = float(input("\nEnter budget: "))
    activities = input("\nEnter activities (comma-separated): ").split(",")

    if not validate(date, budget) :
        print("\nSome of the parameters are not valid!")
        return
    new_trip = Trip(start_city, destination, date, budget, activities)
    trip_list.append(new_trip)
    print("\nTrip added successfully.")

def view_trips(trip_list: List[Trip]):
    """
    Displays the information for all trips in the trip list.

    :param trip_list: List of Trip objects to display
    """
    if not trip_list:
        print("\nNo trips added yet.")
    else:
        for index, trip in enumerate(trip_list):
            print(f"\nTrip {index + 1}:")
            print(f"Start City: {trip.start_city}")
            print(f"Destination: {trip.destination}")
            print(f"Dates: {trip.date}")
            print(f"Budget: {trip.budget}")
            print(f"Activities: {', '.join(trip.activities)}")

def delete_trip(trip_list: List[Trip], index: int):
    """
    Deletes a trip from the trip list based on user input.

    :param index: List of Trip objects to delete
    :param trip_list: List of Trip objects to delete
    """
    if not trip_list:
        print("No trips added yet.")
    else:
        view_trips(trip_list)
        try:
            if 0 <= index < len(trip_list):
                trip_list.pop(index)
                print("\nTrip deleted successfully.")
            else:
                print("\nInvalid index.")
        except ValueError:
            print("\nInvalid input. Please enter a valid index.")
def filter_trips(trips_list: List[Trip], key: int, value: Union[str, float]) -> List[Trip]:
    """
    Filters trips from the trips_list based on the given key and value.

    :param trips_list: List of Trip objects to be filtered
    :param key: Key for filtering trips (1 for date, 2 for budget, 3 for destination)
    :param value: Value for filtering trips
    :return: List of Trip objects filtered by value
    """
    filtered_trips = []
    if key == "1":
        filtered_trips = [trip for trip in trips_list if trip.date == value]
    elif key == "2":
        filtered_trips = [trip for trip in trips_list if trip.budget == float(value)]
    elif key == "3":
        filtered_trips = [trip for trip in trips_list if trip.destination == value]
    else:
        print("\nIncorrect choice!")

    return filtered_trips

def sort_trips(trips_list: List[Trip], key: int) -> List[Trip]:
    """
    Sorts the list of trips based on the specified key.
    :param trips_list: List of Trip objects to be sorted
    :param key: Key which is the sorting criteria (1 - by budget, 2 - by date)
    :return: Sorted list of Trip list
    """
    if key == "1":
        sorted_trips = sorted(trips_list, key=lambda trip: trip.budget)
    elif key == "2":
        sorted_trips = sorted(trips_list, key=lambda trip: trip.date)
    else:
        print("\nIncorrect choice!")
    return sorted_trips

def get_ticket_price_for_trip(trip_index: int,
                              trips_list: List[Trip],
                              travel_api: TravelAPI) -> float:
    """
    Calls API for receiving ticket price for a specific trip and date.

    :param trip_index: Index of the trip to consider
    :param trips_list: List of Trip objects containing the trips
    :param travel_api: Instance of TravelAPI class for API calls
    :return: Result of API"s request for ticket price (lowest ticket price)
    """
    if trip_index > len(trips_list):
        print("\nInvalid input!")
        return 0.0

    trip = trips_list[trip_index - 1]
    if not trip:
        print("\nThere is no such a trip!")
        return 0.0

    ticket_info = travel_api.get_ticket_info(trip.start_city, trip.destination, trip.date)
    if not ticket_info:
        print("\nFailed to retrieve ticket price information!")
        return 0.0

    ticket_price = float(ticket_info["price"]) * 2
    if trip.budget - ticket_price < 0:
        print("\nYour budget is not enough for travelling to that point!")
    return ticket_price

def handle_command(choice: str,
                   trips_list: List[Trip],
                   travel_api: TravelAPI) -> Tuple[bool, List[Trip]]:
    """
    Handles user commands and executes corresponding actions.

    :param choice: User"s choice
    :param trips_list: List of Trip objects
    :param travel_api: Instance of TravelAPI class for API calls
    :return: True if the program should exit, False otherwise
    """

    if choice == "add":
        add_trip(trips_list)
    elif choice == "view":
        view_trips(trips_list)
    elif choice == "delete":
        index = int("\nEnter which trip you want to delete: ") - 1
        delete_trip(trips_list, index)
    elif choice == "filter":
        key = input("\nEnter a way of filtering : \n\t1.date \n\t2.budget \n\t3.destination\n: ")
        value = input("\nEnter the value for filtering the trip: ")
        view_trips(filter_trips(trips_list, key, value))
    elif choice == "sort":
        key = input("\nEnter a way of sorting : \n\t1.budget \n\t2.date\n: ")
        view_trips(sort_trips(trips_list, key))
    elif choice == "export":
        export_to_json(trips_list)
    elif choice == "import":
        trips_list = import_from_json()
    elif choice == "ticket-price":
        trip_index = input("\nEnter which trip's expense you want to see: ")
        ticket_price = get_ticket_price_for_trip(int(trip_index), trips_list, travel_api)
        if ticket_price > 0:
            print(f"\nPrice: {ticket_price}")
    elif choice == "exit":
        return True, trips_list
    else:
        print("\nPlease enter a valid command!")

    return False, trips_list
