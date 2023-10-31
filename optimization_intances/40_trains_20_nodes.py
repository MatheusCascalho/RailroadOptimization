import numpy as np
from optimizer.restrictions.railroad_elements import Flow, TransitTime, Demand, ExchangeBand, Node
from optimizer.optimization_model import RailroadOptimizationProblem
import random

seed_value = 45
random.seed(seed_value)


def build_nodes(amount=2, capacity_interval=(500, 800)):
    capacities = [random.randint(*capacity_interval) for _ in range(amount)]
    nodes = [
        Node(name=f"terminal_{i}", capacity=c)
        for i, c in enumerate(capacities)
    ]
    return nodes


def build_flows(nodes: list[Node], train_capacity_interval: tuple=(50, 80)):
    flows = []
    for origin in nodes:
        for destination in nodes:
            if origin == destination:
                continue
            flow = Flow(
                origin=origin,
                destination=destination,
                train_volume=random.randint(*train_capacity_interval)
            )
            flows.append(flow)
    return flows


def build_transits(flows: list[Flow], transit_interval=(2, 5)):
    transits = []

    for i, flow in enumerate(flows):
        transit = TransitTime(
            origin=flow.origin,
            destination=flow.destination,
            time=round(random.uniform(*transit_interval), 2)
        )
        transits.append(transit)
    return transits


def build_demands(flows: list[Flow], demand_interval=(2e3, 50e3), with_minimum=.2):
    demands = []
    flows_with_minimum = np.floor(len(flows)*with_minimum)

    for i, flow in enumerate(flows):
        minimum = np.random.uniform(*demand_interval)
        maximum = np.random.uniform(*demand_interval)
        if i < flows_with_minimum:

            if maximum < minimum:
                aux = maximum
                maximum = minimum
                minimum = aux
            if flow.origin.capacity < minimum:
                minimum = flow.origin.capacity
        else:
            minimum=0
        transit = Demand(
            flow=flow,
            minimum=minimum,
            maximum=maximum
        )
        demands.append(transit)
    return demands



nodes = build_nodes(amount=10, capacity_interval=(10e6, 10e6))
flows = build_flows(nodes=nodes)
demand = build_demands(flows=flows, with_minimum=0)
transit = build_transits(flows=flows, transit_interval=(1, 2))


problem = RailroadOptimizationProblem(
    trains=40,
    transit_times=transit,
    demands=demand,
    exchange_bands=[],
    time_horizon=90
)
# print(problem)

