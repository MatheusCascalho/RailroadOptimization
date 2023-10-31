"""
This file builds the Railroad Optimization Problem in the format to be used in Gurobi solver

"""
import numpy as np
import gurobipy as gp
from optimizer.restrictions.railroad_elements import Flow, TransitTime, Demand, ExchangeBand, Node
from optimizer.restrictions.restrictions import Restrictions, RestrictionType, Restriction
from optimizer.restrictions.capacity_restriction import CapacityRestrictions
from optimizer.restrictions.exchange_restriction import ExchangeRestriction
from optimizer.restrictions.time_horizon_restriction import TimeHorizonRestriction
from optimizer.restrictions.demand_restriction import MaximumDemandRestriction, MinimumDemandRestriction


class RailroadOptimizationProblem:
    def __init__(
            self,
            trains: int,
            demands: list[Demand],
            transit_times: list[TransitTime],
            exchange_bands: list[ExchangeBand],
            time_horizon: int
    ):
        # Building constraints
        flows = [d.flow for d in demands]
        self.trains = trains
        self.capacity = CapacityRestrictions(trains=trains, flows=flows)
        self.exchange = ExchangeRestriction(trains=trains, bands=exchange_bands, flows=flows)
        self.time_horizon = TimeHorizonRestriction(
            trains=trains,
            transit_times=transit_times,
            flows=flows,
            time_horizon=time_horizon
        )
        self.minimum_demand = MinimumDemandRestriction(trains=trains, demands=demands)
        self.maximum_demand = MaximumDemandRestriction(trains=trains, demands=demands)
        self.costs = sum([r.coefficients for r in self.maximum_demand.restrictions()])

        self.geq_constraints = []
        self.geq_constraints.extend(self.capacity.restrictions())
        self.geq_constraints.extend(self.exchange.restrictions())
        self.geq_constraints.extend(self.time_horizon.restrictions())
        self.geq_constraints.extend(self.maximum_demand.restrictions())

        self.leq_constraints = []
        self.leq_constraints.extend(self.minimum_demand.restrictions())

        labels = self.labels()

        # Building GUROBI model
        model = gp.Model("Railroad Optimization Problem")
        # model.setParam('OutputFlag', 0)
        x = model.addVars(
            labels,
            vtype=gp.GRB.INTEGER
        )
        model.setObjective(
            expr=gp.quicksum([x[i] * self.costs[i] for i in x]),
            sense=gp.GRB.MAXIMIZE
        )

        for r in self.geq_constraints:
            model.addConstr(gp.quicksum([x[i] * r.coefficients[i] for i in labels]) <= r.resource)
        for r in self.leq_constraints:
            model.addConstr(gp.quicksum([x[i] * r.coefficients[i] for i in labels]) >= r.resource)

        print(model.optimize())

        if model.status == gp.GRB.OPTIMAL:
            print("="*50)
            matrix = np.zeros(self.capacity.cardinality)
            for label in labels:
                matrix[label] = x[label].X
            result = np.sum(matrix, axis=(0, 1))
            demanda = round(sum(d.resource for d in self.maximum_demand.restrictions()), 1)
            print(f"Demanda: {demanda} | Aceite ótimo: {model.objVal}\n")
            for j, origin in enumerate(self.maximum_demand.loaded_origins):
                for k, destination in enumerate(self.maximum_demand.loaded_destinations):
                    travels = result[j, k]
                    if travels:
                        print(f"{origin}->{destination}: {travels} travels")

            print("="*50)

    def labels(self):
        # Building vars label
        labels = []
        for n in range(self.trains):
            for i, e_origin in enumerate(self.capacity.empty_origins):
                for j, l_origin in enumerate(self.capacity.loaded_origins):
                    for k, l_destination in enumerate(self.capacity.loaded_destinations):
                        # label = f"train_{n}-empty_{i}-from_{j}_to-{k}"
                        label = (n, i, j, k)
                        labels.append(label)
        return labels

    def __repr__(self):
        repr = f"Problem with {len(self.geq_constraints+self.leq_constraints)} constraints and {len(self.labels())} variables\n\n"
        for r in self.geq_constraints+self.leq_constraints:
            lhs = ""
            for i in self.labels():
                if r.coefficients[i] != 0:
                    lhs += str(r.coefficients[i]) + f"*x_{'|'.join([str(x) for x in i])} " + "\t\t"
            lhs = lhs[:-1].replace("\t\t", "\t+")
            repr += f"{lhs} {r.sense}= {r.resource} \n"

        return repr


if __name__=='__main__':
    n1 = Node(name='terminal 1', capacity=500)
    n2 = Node(name='terminal 2', capacity=600)
    n3 = Node(name='terminal 3', capacity=600)
    f1 = Flow(
        origin=n1,
        destination=n2,
        train_volume=50
    )
    f2 = Flow(
        origin=n1,
        destination=n3,
        train_volume=60
    )

    demands = [
        Demand(flow=f1, minimum=200, maximum=50e3),
        Demand(flow=f2, minimum=100, maximum=40e3),
    ]

    transit_times = [
        TransitTime(origin=n1, destination=n2, time=2.5),
        TransitTime(origin=n1, destination=n3, time=3.9),
    ]
    problem = RailroadOptimizationProblem(
        trains=1,
        transit_times=transit_times,
        demands=demands,
        exchange_bands=[],
        time_horizon=90
    )
    print(problem)

