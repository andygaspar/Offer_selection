import numpy as np

from objects.airline import Airline
from objects.flight import Flight


def make_flights(airlines_names, cost_coefficients, cost_kind="quad", show=False):
    airlines = [Airline(air_name) for air_name in np.unique(airlines_names)]
    airlines_dict = dict(zip([air.name for air in airlines], airlines))
    flights = []
    for i in range(len(airlines_names)):
        flights.append(Flight(i, airlines_dict[airlines_names[i]], cost_coefficients[i], cost_kind))
    if show:
        for flight in flights:
            print(flight, flight.airline, flight.index, flight.cost, flight.eta)
    return flights, airlines
