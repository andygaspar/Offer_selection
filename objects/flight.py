import numpy as np

from input import num_flights


class Flight:

    def __init__(self, index, airline, cost_coefficient, cost_kind="quad"):
        self.name = "F" + airline.name + str(index)
        self.airline = airline
        self.airline.flights.append(self)
        self.index = index
        self.cost = cost_coefficient
        self.eta = index
        self.sol = None
        if cost_kind == "quad":
            cost_fun = lambda delay: 0 if delay < 0 else self.cost * delay ** 2
        else:
            cost_fun = lambda delay: 0 if delay < 0 else self.cost * delay
        self.costVect = np.array([cost_fun(t - self.eta) for t in np.arange(0, num_flights * 2, 2)])

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
