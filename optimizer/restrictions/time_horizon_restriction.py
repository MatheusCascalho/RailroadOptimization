import numpy as np
from optimizer.restrictions.railroad_elements import Flow, TransitTime, RailroadProblemTemplate
from optimizer.restrictions.restrictions import Restrictions, RestrictionType, Restriction


class TimeHorizonRestriction(RailroadProblemTemplate, Restrictions):
    def __init__(
            self,
            trains,
            transit_times: list[TransitTime],
            flows: list[Flow],
            time_horizon: int
    ):
        super().__init__(
            trains=trains,
            flows=flows
        )
        self.__restrictions = self.__build_restrictions(transit_times=transit_times, time_horizon=time_horizon)

    def __build_restrictions(self, transit_times: list[TransitTime], time_horizon: int) -> list[Restriction]:
        restrictions = []
        transit_matrix = self.__build_transit_matrix(transit_times=transit_times)

        for n in range(self.cardinality[0]):
            matrix = np.zeros(self.cardinality)
            for j in range(len(self.loaded_origins)):
                for k in range(len(self.loaded_destinations)):
                    time = transit_matrix[j, k]
                    matrix[n, :, j, k] += time
                    matrix[n, k, j, :] += time
            restriction = Restriction(
                coefficients=matrix,
                sense=self.restriction_type.value,
                resource=time_horizon
            )
            restrictions.append(restriction)
        return restrictions

    def __build_transit_matrix(self, transit_times: list[TransitTime]) -> np.ndarray:
        l = len(self.loaded_origins)
        u = len(self.loaded_destinations)
        shape = (l, u)
        matrix = np.zeros(shape)
        for transit in transit_times:
            if transit.origin in self.loaded_origins:
                j = self.loaded_origins.index(transit.origin)
                k = self.loaded_destinations.index(transit.destination)
                matrix[j, k] = transit.time
        return matrix

    def restrictions(self) -> list[Restriction]:
        return self.__restrictions

    @property
    def restriction_type(self) -> RestrictionType:
        return RestrictionType.LESS_OR_EQUAL
