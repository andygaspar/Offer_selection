import gurobipy as gb
import numpy as np
from gurobipy import GRB, quicksum


class OfferEval:

    def __init__(self, offer, new_slot_times):
        self.p = gb.Model()
        self.p.modelSense = GRB.MINIMIZE
        self.offer = offer
        self.eps = 0.01
        self.indexes_a = offer.indexes_a
        self.indexes_b = offer.indexes_b
        self.switch_ab = np.array([(i, j) for i in self.indexes_a for j in self.indexes_b])
        self.switch_ba = np.array([(j, i) for i in self.indexes_a for j in self.indexes_b])
        self.indexes = offer.indexes_both
        self.new_slot_times = new_slot_times
        self.p.setParam('OutputFlag', 0)
        self.x = self.p.addVars([np.concatenate((self.switch_ab, self.switch_ba))], vtype=GRB.BINARY)

    def set_constraints(self):
        for i in self.indexes_a:
            self.p.addConstr(quicksum(self.x[i, j] for j in self.indexes_b) == 1, name="c1[%s]" % i)
            self.p.addConstr(quicksum(self.x[j, i] for j in self.indexes_b) == 1, name="c2[%s]" % i)
        for i in self.indexes_b:
            self.p.addConstr(quicksum(self.x[i, j] for j in self.indexes_a) == 1, name="c1[%s]" % i)
            self.p.addConstr(quicksum(self.x[j, i] for j in self.indexes_a) == 1, name="c2[%s]" % i)
        for flight_a in self.offer.flights_a:
            self.p.addConstr(quicksum(
                self.x[flight_a.index, j] for j in self.indexes_b if self.new_slot_times[j] < flight_a.eta) == 0,
                             name="c3[%s]" % flight_a)
        for flight_b in self.offer.flights_b:
            self.p.addConstr(quicksum(
                self.x[flight_b.index, j] for j in self.indexes_a if self.new_slot_times[j] < flight_b.eta) == 0,
                             name="c3[%s]" % flight_b)
        self.p.addConstr(quicksum(
            self.x[flight.index, j] * flight.normcostVect[j] for flight in self.offer.flights_a for j in
            self.indexes_b) <= quicksum(
            flight.normcostVect[flight.index] for flight in self.offer.flights_a) - self.eps,
                         name="c4a")
        self.p.addConstr(quicksum(
            self.x[flight.index, j] * flight.normcostVect[j] for flight in self.offer.flights_b for j in
            self.indexes_a) <= quicksum(
            flight.normcostVect[flight.index] for flight in self.offer.flights_b) - self.eps,
                         name="c4b")

    def set_objective(self):
        self.p.setObjective(
            quicksum(self.x[flight.index, j] * flight.normCostVect[j] for flight in self.offer.flights_a for j in
                     self.indexes_b) + quicksum(
                self.x[flight.index, j] * flight.normCostVect[j] for flight in self.offer.flights_b for j in
                self.indexes_a))

    def solve(self):
        self.set_constraints()
        self.set_objective()
        self.p.optimize()
        #se feasible --> salvare objval come costo offerta e quale scambio avviene fra i possibili
        #altrimenti verrà scartata l'offerta
