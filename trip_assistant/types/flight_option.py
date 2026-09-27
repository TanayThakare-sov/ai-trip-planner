from typing import TypedDict

class FlightOption(TypedDict):
    airline: str
    flight_number: str
    departure_time: str
    arrival_time: str
    duration: str
    price: float