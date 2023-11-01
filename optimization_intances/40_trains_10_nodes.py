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



nodes = build_nodes(amount=10, capacity_interval=(30*4e3, 5*30*8e3))
flows = build_flows(nodes=nodes, train_capacity_interval=(4e3, 8e3))
demand = build_demands(flows=flows, with_minimum=0, demand_interval=(10e3, 500e3))
transit = build_transits(flows=flows, transit_interval=(1, 2))


problem = RailroadOptimizationProblem(
    trains=40,
    transit_times=transit,
    demands=demand,
    exchange_bands=[],
    time_horizon=90,
    max_time=10*60
)
print(problem)
""" Output
Academic license - for non-commercial use only - expires 2024-10-28
Gurobi Optimizer version 10.0.3 build v10.0.3rc0 (linux64)

CPU model: Intel(R) Core(TM) i7-8565U CPU @ 1.80GHz, instruction set [SSE2|AVX|AVX2]
Thread count: 4 physical cores, 8 logical processors, using up to 8 threads

Optimize a model with 280 rows, 40000 columns and 4320000 nonzeros
Model fingerprint: 0xad767afd
Variable types: 0 continuous, 40000 integer (0 binary)
Coefficient statistics:
  Matrix range     [1e+00, 8e+01]
  Objective range  [5e+01, 8e+01]
  Bounds range     [0e+00, 0e+00]
  RHS range        [9e+01, 1e+07]
Found heuristic solution: objective 2875.0000000
Presolve removed 279 rows and 39997 columns
Presolve time: 3.52s
Presolved: 1 rows, 3 columns, 3 nonzeros
Found heuristic solution: objective 6160.0000000
Variable types: 0 continuous, 3 integer (0 binary)

Root relaxation: objective 6.815250e+03, 1 iterations, 0.00 seconds (0.00 work units)

    Nodes    |    Current Node    |     Objective Bounds      |     Work
 Expl Unexpl |  Obj  Depth IntInf | Incumbent    BestBd   Gap | It/Node Time

     0     0 6815.25000    0    1 6160.00000 6815.25000  10.6%     -    3s
H    0     0                    6788.0000000 6815.25000  0.40%     -    3s
H    0     0                    6792.0000000 6815.25000  0.34%     -    3s
     0     0 6814.80583    0    1 6792.00000 6814.80583  0.34%     -    3s
     0     2 6814.80583    0    1 6792.00000 6814.80583  0.34%     -    3s
H   67     3                    6798.0000000 6800.25000  0.03%   0.7    3s

Explored 72 nodes (56 simplex iterations) in 3.69 seconds (1.57 work units)
Thread count was 8 (of 8 available processors)

Solution count 5: 6798 6792 6788 ... 2875

Optimal solution found (tolerance 1.00e-04)
Best objective 6.798000000000e+03, best bound 6.798000000000e+03, gap 0.0000%
None
==================================================
Demanda: 2366141.4 | Aceite ótimo: 6798.0

1-terminal_1->8-terminal_8: 22.0 travels
5-terminal_5->7-terminal_7: 66.0 travels
==================================================

Process finished with exit code 0
"""

