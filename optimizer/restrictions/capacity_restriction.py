from dataclasses import dataclass, field
import numpy as np
from optimizer.restrictions.restrictions import Restrictions, RestrictionType, Restriction


def node_id_generator():
    identifier = 0
    while True:
        yield identifier
        identifier += 1


class Node:
    __id_generator = node_id_generator()

    def __init__(self, name: str, capacity: float):
        self.name = name
        self.capacity = capacity
        self.identifier = next(self.__id_generator)

    def __repr__(self):
        return f"{self.identifier}-{self.name}"

    __str__ = __repr__


@dataclass
class Flow:
    origin: Node
    destination: Node
    train_volume: float


class CapacityRestrictions(Restrictions):
    def __init__(
            self,
            trains: int,
            flows: list[Flow]
    ):
        self.__trains = trains
        self.__empty_origins = self.build_unload_points(flows=flows)
        self.__loaded_origins = self.build_load_points(flows=flows)
        self.__loaded_destinations = self.build_unload_points(flows=flows)
        u = len(self.__loaded_destinations)
        l = len(self.__loaded_origins)
        self.__cardinality = (self.__trains, u, l, u)
        self.__restrictions = self.__build_restrictions(flows=flows)

    def __build_restrictions(self, flows):
        restrictions = []
        for j, origin in enumerate(self.__loaded_origins):
            matrix = np.zeros(self.__cardinality)
            filtered_flows = [flow for flow in flows if flow.origin == origin]
            if filtered_flows:
                for flow in filtered_flows:
                    coefficient = flow.train_volume
                    k = self.__loaded_destinations.index(flow.destination)
                    matrix[:, :, j, k] = coefficient
                    restriction = Restriction(
                        coefficients=matrix,
                        sense=self.restriction_type.value,
                        resource=origin.capacity
                    )
                restrictions.append(restriction)
        return restrictions

    def restrictions(self) -> list[Restriction]:
        return self.__restrictions

    @staticmethod
    def build_unload_points(flows: list[Flow]):
        nodes = set([f.destination for f in flows])
        nodes = sorted(nodes, key=lambda x: x.identifier)
        return nodes

    @staticmethod
    def build_load_points(flows: list[Flow]):
        nodes = set([f.origin for f in flows])
        nodes = sorted(nodes, key=lambda x: x.identifier)
        return nodes

    @property
    def restriction_type(self) -> RestrictionType:
        return RestrictionType.LESS_OR_EQUAL

    @property
    def cardinality(self):
        return self.__cardinality
