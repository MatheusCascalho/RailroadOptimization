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
        capacity = CapacityRestrictions(trains=trains, flows=flows)
        exchange = ExchangeRestriction(trains=trains, bands=exchange_bands, flows=flows)
        time_horizon = TimeHorizonRestriction(
            trains=trains,
            transit_times=transit_times,
            flows=flows,
            time_horizon=time_horizon
        )
        minimum_demand = MinimumDemandRestriction(trains=trains, demands=demands)
        maximum_demand = MaximumDemandRestriction(trains=trains, demands=demands)
        self.constraints = []
        self.constraints.extend(capacity.restrictions())

        # Building vars label
        labels = []
        for n in range(trains):
            for i, e_origin in enumerate(capacity.empty_origins):
                for j, l_origin in enumerate(capacity.loaded_origins):
                    for k, l_destination in enumerate(capacity.loaded_destinations):
                        # label = f"train_{n}-empty_{i}-from_{j}_to-{k}"
                        label = (n, i, j, k)
                        labels.append(label)



        # Building GUROBI model
        model = gp.Model("Railroad Optimization Problem")
        x = model.addVars(
            labels,
            vtype=gp.GRB.INTEGER
        )
        model.setObjective(
            expr=gp.quicksum([x.values()[i] * np.sum(maximum_demand.coefficients_matrix, axis=0)[i] for i in range(len(labels))]),
            sense=gp.GRB.MAXIMIZE
        )
        print(model)


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
        Demand(flow=f1, minimum=30e3, maximum=50e3),
        Demand(flow=f2, minimum=20e3, maximum=40e3),
    ]

    transit_times = [
        TransitTime(origin=n1, destination=n2, time=20),
        TransitTime(origin=n1, destination=n3, time=30),
    ]
    problem = RailroadOptimizationProblem(
        trains=1,
        transit_times=transit_times,
        demands=demands,
        exchange_bands=[],
        time_horizon=90
    )
    print(problem)

