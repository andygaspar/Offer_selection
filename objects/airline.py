from objects.functions import initial_costs


class Airline:

    def __init__(self, name):
        self.name = name
        self.initial_costs = None
        self.final_costs = None
        self.reduction = None
        self.reduction_percentage = None
        self.flights = []

    def __str__(self):
        return self.name

    def compute_costs(self):
        self.initial_costs = initial_costs(self.flights)
        self.final_costs = sum([flight.costVect[flight.sol] for flight in self.flights])
        self.reduction = self.final_costs - self.initial_costs
        self.reduction_percentage = self.reduction / self.initial_costs
