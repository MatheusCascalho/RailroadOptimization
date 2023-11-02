import random

import numpy as np

from optimizer.restrictions.railroad_elements import Node, Flow, TransitTime, Demand

seed_value = 45
random.seed(seed_value)


def build_nodes(amount=2, capacity_interval=(500, 800)):
    capacities = [random.randint(*capacity_interval) for _ in range(amount)]
    nodes = [
        Node(name=f"terminal_{i}", capacity=c)
        for i, c in enumerate(capacities)
    ]
    return nodes

def build_terminals_and_ports(terminals=1, ports=1, capacity_interval=(500, 800)):
    capacities = [random.randint(*capacity_interval) for _ in range(terminals)]
    terminals = [
        Node(name=f"terminal_{i}", capacity=c)
        for i, c in enumerate(capacities)
    ]
    capacities = [random.randint(*capacity_interval) for _ in range(ports)]
    ports = [
        Node(name=f"port_{i}", capacity=c)
        for i, c in enumerate(capacities)
    ]
    return terminals

def build_flows(nodes: list[Node], train_capacity_interval: tuple=(5e3, 8e3)):
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


def build_demands(flows: list[Flow], demand_interval=(20e3, 50e3), with_minimum=.2):
    demands = []
    flows_with_minimum = np.floor(len(flows)*with_minimum)

    for i, flow in enumerate(flows):
        maximum = np.random.uniform(*demand_interval)
        minimum = flow.train_volume  # at least one train should be used in this flow
        if i < flows_with_minimum:

            if maximum < minimum:
                aux = maximum
                maximum = minimum
                minimum = aux
            if flow.origin.capacity < minimum:
                minimum = flow.origin.capacity * 0.1
        else:
            minimum=0
        transit = Demand(
            flow=flow,
            minimum=minimum,
            maximum=maximum
        )
        demands.append(transit)
    return demands
