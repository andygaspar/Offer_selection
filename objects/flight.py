import numpy as np

from input import new_slot_times


class Flight:

    def __init__(self, index, slot, airline, cost_coefficient, cost_kind="quad"):
        self.name = "F" + airline.name + str(index)
        self.airline = airline
        self.airline.flights.append(self)
        self.index = index
        self.cost = cost_coefficient
        self.eta = slot
        self.cost_kind = cost_kind
        self.sol = None
        self.norm_cost = None
        self.normCostVect = None

        if cost_kind == "quad":
            cost_fun = lambda delay: 0 if delay < 0 else self.cost * delay ** 2
        else:
            cost_fun = lambda delay: 0 if delay < 0 else self.cost * delay

        self.costVect = np.array([cost_fun(t - self.eta) for t in new_slot_times])

    def normalise(self, max_cost):
        self.norm_cost = self.cost / max_cost
        if self.cost_kind == "quad":
            norm_cost_fun = lambda delay: 0 if delay < 0 else self.norm_cost * delay ** 2
        else:
            norm_cost_fun = lambda delay: 0 if delay < 0 else self.norm_cost * delay
        self.normCostVect = np.array([norm_cost_fun(t - self.eta) for t in new_slot_times])

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
