from input import *
from models.min_cost import Min_cost
from objects.initializer import make_flights

flights, airline_list = make_flights(airlines_name, cost_coefficients)
min_cost = Min_cost(flights, airline_list, slots, new_slot_times)
min_cost.solve()
nnb = Min_cost(flights, airline_list, slots, new_slot_times, nnb=True)
nnb.solve()
