def sum_costs(flights, initial=True):
    return sum([flight.costVect[flight.index if initial else flight.sol] for flight in flights])
