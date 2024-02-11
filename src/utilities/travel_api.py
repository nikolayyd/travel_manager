"""
Module containing the TravelAPI class for interacting with the Aviasales API
and a function for getting city codes.
"""

from typing import Dict
import csv
import os
import requests

class TravelAPI:
    """Represents an interface for interacting with a travel API."""
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.travelpayouts.com/v1/prices/cheap"

    def update_api_key(self, new_api_key: str):
        """
        Updates the API key used for requests.
        :param new_api_key: The new API key to use.
        """
        self.api_key = new_api_key

    def get_ticket_info(self, origin: str, destination: str, depart_date: str) -> Dict:
        """
        Calls Aviasales API for receiving the cheapest tickets for given
        origin, destination, and departure date.
        :param origin: Origin city or airport code
        :param destination: Destination city or airport code
        :param depart_date: Departure date in the format "YYYY-MM-DD"
        :return: Dict with cheapest ticket information
        """
        endpoint = self.base_url
        iata_origin = get_city_code(origin)
        iata_destination = get_city_code(destination)
        params = {
            "origin": iata_origin,
            "destination": iata_destination,
            "depart_date": depart_date,
            "currency": "eur",
            "token": self.api_key
        }

        response = requests.get(endpoint, params=params)
        if response.status_code != 200:
            print("\nError with extracting tickets' prices.")
            return []

        data = response.json()
        if ("data" not in data or
            iata_destination not in data["data"] or
            "0" not in data["data"][iata_destination]):
            print("\nNo ticket data found in response.")
            return []

        ticket_info = data["data"][iata_destination]["0"]
        return ticket_info


def get_city_code(city_name: str) -> str:
    """
    Returns the city code based on the provided city name.

    :param city_name: The name of the city.
    :return: The city code.
    """

    file_path = os.path.join(os.path.dirname(__file__),"city_codes.csv")
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if "/" in row[1]:
                city_parts = row[1].split("/")
                if len(city_parts) == 2 and city_parts[1].strip().lower() == city_name.lower():
                    return row[0].strip()
    return ""
