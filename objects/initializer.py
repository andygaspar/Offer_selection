import numpy as np

from input import slots
from objects.airline import Airline
from objects.flight import Flight
from objects.offer import Offer


def make_flights(airlines_names, cost_coefficients, cost_kind="quad", show=False):
    airlines = [Airline(air_name) for air_name in np.unique(airlines_names)]
    airlines_dict = dict(zip([air.name for air in airlines], airlines))
    flights = []
    for i in range(len(airlines_names)):
        flights.append(
            Flight(i, slots[i], airlines_dict[airlines_names[i]], cost_coefficients[i], cost_kind))
    if show:
        for flight in flights:
            print(flight, flight.airline, flight.index, flight.cost, flight.eta)
    for air in airlines:
        normalise_flights(air)
    return flights, airlines


def normalise_flights(airline):
    max_cost = max([flight.cost for flight in airline.flights])
    for flight in airline.flights:
        flight.normalise(max_cost)


def make_couples_air(airline_list):
    couples = []
    for i in range(len(airline_list)):
        for j in range(i + 1, len(airline_list)):
            couples.append((airline_list[i], airline_list[j]))
    return couples


def make_offers(offers_list, air_couple):
    air_a = air_couple[0]
    air_b = air_couple[1]
    num_a = len(air_a.flights_couples)
    num_b = len(air_b.flights_couples)
    for i in range(num_a):
        for j in range(num_b):
            number = len(offers_list)
            flights_a_list = []
            flights_b_list = []
            flights_a_list.extend([air_a.flights_couples[i][0], air_a.flights_couples[i][1]])
            flights_b_list.extend([air_b.flights_couples[j][0], air_b.flights_couples[j][1]])
            offer = Offer(number, air_a, air_b, flights_a_list, flights_b_list)
            offers_list.append(offer)
