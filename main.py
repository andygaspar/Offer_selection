from input import *
from models.mincost import MinCost
from objects.initializer import *

flights, airline_list = make_flights(airlines_name, cost_coefficients)

couples = make_couples_air(airline_list)
print(couples)
for airline in airline_list:
    airline.make_flights_couples()
offers_list = []
for couple in couples:
    make_offers(offers_list, couple)
print(offers_list)

min_cost = MinCost(flights, airline_list, indexes, new_slot_times)
min_cost.solve()
nnb = MinCost(flights, airline_list, indexes, new_slot_times, nnb=True)
nnb.solve()
