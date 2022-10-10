import gurobipy as gb
from gurobipy import GRB, quicksum

from objects.functions import sum_costs


class MinCost:

    def __init__(self, flights, airlines, indexes, new_slot_times, nnb=False):
        self.p = gb.Model()
        self.p.modelSense = GRB.MINIMIZE
        self.airlines = airlines
        self.flights = flights
        self.indexes = indexes
        self.new_slot_times = new_slot_times
        self.p.setParam('OutputFlag', 0)
        self.x = self.p.addVars([(flight.index, j) for j in indexes for flight in flights], vtype=GRB.BINARY)
        self.nnb = nnb
        self.reduction = None

    def set_constraints(self):
        for flight in self.flights:
            self.p.addConstr(quicksum(self.x[flight.index, j] for j in self.indexes) == 1, name="c1[%s]" % flight)
            self.p.addConstr(
                quicksum(self.x[flight.index, j] for j in self.indexes if self.new_slot_times[j] < flight.eta) == 0,
                name="c2[%s]" % flight)

        for j in self.indexes:
            self.p.addConstr(quicksum(self.x[flight.index, j] for flight in self.flights) <= 1, name="c3[%s]" % j)

        if self.nnb:
            for air in self.airlines:
                self.p.addConstr(
                    quicksum(self.x[flight.index, j] * flight.costVect[j] for flight in air.flights for j in
                             self.indexes) <= sum_costs(air.flights), name="c4[%s]" % air)

    def set_objective(self):
        self.p.setObjective(
            quicksum(self.x[flight.index, j] * flight.costVect[j] for flight in self.flights for j in self.indexes))

    def solve(self):
        self.set_constraints()
        self.set_objective()
        self.p.optimize()

        print("flight  cost  index  airline  delay")
        for j in self.indexes:
            for flight in self.flights:
                if round(self.x[flight.index, j].x) == 1:
                    flight.sol = j
                    print(flight, flight.cost, j, flight.airline, self.new_slot_times[j] - flight.eta)

        total_initial = sum_costs(self.flights)
        total_final = self.p.objVal
        total_reduction = (total_initial - total_final) / total_initial
        self.reduction = total_reduction
        print("\ninitial cost:", total_initial)
        print("final cost:", total_final)
        print("reduction", total_reduction, "\n")

        for air in self.airlines:
            air.compute_costs()
            print("Airline Company: ", air.name, "\nInitial cost: ", air.initial_costs, "Final cost: ", air.final_costs)
        print("\n")
