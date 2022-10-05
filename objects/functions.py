def initial_costs(flights):
    return sum([flight.costVect[flight.eta] for flight in flights])
