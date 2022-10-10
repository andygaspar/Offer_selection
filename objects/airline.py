from objects.functions import sum_costs


class Airline:

    def __init__(self, name):
        self.name = name
        self.initial_costs = None
        self.final_costs = None
        self.reduction = None
        self.reduction_percentage = None
        self.flights = []
        self.flights_couples = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def compute_costs(self):
        self.initial_costs = sum_costs(self.flights)
        self.final_costs = sum_costs(self.flights, False)
        self.reduction = self.final_costs - self.initial_costs
        self.reduction_percentage = self.reduction / self.initial_costs

    def make_flights_couples(self):
        for i in range(len(self.flights)):
            for j in range(i + 1, len(self.flights)):
                self.flights_couples.append((self.flights[i], self.flights[j]))
