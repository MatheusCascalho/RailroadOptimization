from optimization_intances.instances_creator import seed_value, build_nodes, build_flows, build_transits, build_demands
from optimizer.optimization_model import RailroadOptimizationProblem

nodes = build_nodes(amount=10, capacity_interval=(30 * 8e3, 5 * 30 * 8e3))
flows = build_flows(nodes=nodes, train_capacity_interval=(4e3, 8e3))
demand = build_demands(flows=flows, with_minimum=0.5, demand_interval=(10e3, 500e3))
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