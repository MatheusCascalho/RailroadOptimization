"""
This file declares the restriction interface - class Restriction - and implements each restriction for
railroad optimization problem - ROP

"""

import abc
import numpy as np
from dataclasses import dataclass


@dataclass
class Restriction:
    coefficients: np.ndarray
    sense: str
    resource: float


class Restrictions(abc.ABC):

    @abc.abstractmethod
    def inequality_coefficients(self):
        """
        This method build coefficients of inequality restriction as a Matrix
        :return:
        """
        pass

    @abc.abstractmethod
    def equality_coefficients(self):
        """
        This method build coefficients of equality restriction as a Matrix
        :return:
        """
        pass



