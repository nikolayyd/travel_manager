"""
Module for handling user commands related to trips and travel information.
"""
from src.utilities.command_handler import handle_command
from src.utilities.travel_api import TravelAPI

trips_list = []
API_KEY = "6cdb45d8bd393c8e04f3e5041e5973de"
travel_api = TravelAPI(API_KEY)

while True:
    print("\nList of commands:")
    print("add: Add a trip")
    print("view: View added trips")
    print("delete: Delete a trip")
    print("filter: Filter trips by a specific value")
    print("sort: Sort trips by budget or date")
    print("export: Export trips data to JSON")
    print("import: Import trips data from JSON")
    print("ticket-price: See best price for your trip via API")
    print("exit: Exit")

    choice = input("\nEnter a command: ")

    should_exit, trips_list = handle_command(choice, trips_list, travel_api)
    if should_exit:
        break
