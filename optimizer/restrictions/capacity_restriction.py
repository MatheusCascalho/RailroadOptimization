from dataclasses import dataclass, field
import numpy as np
from optimizer.restrictions.restrictions import Restrictions, RestrictionType


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
        self.__empty_origins = self.build_load_points(flows=flows)
        self.__loaded_origins = self.build_load_points(flows=flows)
        self.__loaded_destinations = self.build_unload_points(flows=flows)

    @staticmethod
    def build_unload_points(flows: list[Flow]):
        nodes = [f.destination for f in flows]
        nodes = sorted(nodes, key=lambda x: x.identifier)
        return nodes

    @staticmethod
    def build_load_points(flows: list[Flow]):
        nodes = [f.origin for f in flows]
        nodes = sorted(nodes, key=lambda x: x.identifier)
        return nodes

    def coefficients_matrix(self) -> np.ndarray:
        pass

    def restriction_type(self) -> RestrictionType:
        pass
