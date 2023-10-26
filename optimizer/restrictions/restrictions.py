"""
This file declares the restriction interface - class Restriction - and implements each restriction for
railroad optimization problem - ROP

"""

import abc
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


class Restrictions(abc.ABC):
    @abc.abstractmethod
    @property
    def restrictions(self):
        pass

    @abc.abstractmethod
    @property
    def restriction_type(self) -> RestrictionType:
        pass

    @abc.abstractmethod
    def coefficients_matrix(self) -> np.ndarray:
        """
        This method build constraint coefficients as a Matrix
        :return:
        """
        pass

    @abc.abstractmethod
    @property
    def cardinality(self):
        pass


