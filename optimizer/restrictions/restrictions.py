"""
This file declares the restriction interface - class Restriction - and implements each restriction for
railroad optimization problem - ROP

"""

from abc import abstractmethod, ABC
import numpy as np
from dataclasses import dataclass
from enum import Enum


class RestrictionType(Enum):
    EQUALITY = "="
    LESS_OR_EQUAL = "<"
    GREATER_OR_EQUAL = ">"
    INEQUALITY = "<>"


@dataclass
class Restriction:
    coefficients: np.ndarray
    sense: str
    resource: float

    def vectorize(self, data):
        for dimension in data:
            if isinstance(dimension, np.ndarray):
                for d in self.vectorize(dimension):
                    yield d
            else:
                yield dimension

    def to_vector(self):
        data = list(self.vectorize(self.coefficients))
        data = np.array(data)
        return data


class Restrictions(ABC):
    @abstractmethod
    def restrictions(self):
        pass

    @abstractmethod
    def restriction_type(self) -> RestrictionType:
        pass

    @abstractmethod
    def coefficients_matrix(self) -> np.ndarray:
        """
        This method build constraint coefficients as a Matrix
        :return:
        """
        pass

    @abstractmethod
    def cardinality(self):
        pass


