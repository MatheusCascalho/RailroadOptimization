from dataclasses import dataclass


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
