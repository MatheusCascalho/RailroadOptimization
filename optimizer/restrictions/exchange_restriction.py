import numpy as np
from optimizer.restrictions.railroad_elements import Flow, ExchangeBand, RailroadProblemTemplate
from optimizer.restrictions.restrictions import Restrictions, RestrictionType, Restriction


class ExchangeRestriction(RailroadProblemTemplate, Restrictions):
    def __init__(
            self,
            trains,
            bands: list[ExchangeBand],
            flows: list[Flow]
    ):
        super().__init__(
            trains=trains,
            flows=flows
        )
        self.__restrictions = self.__build_restrictions(bands=bands)

    def __build_restrictions(self, bands) -> list[Restriction]:
        restrictions = []
        for k, node in enumerate(self.loaded_destinations):
            matrix = np.zeros(self.cardinality)
            filtered_bands = [b for b in bands if b.node == node]
            if filtered_bands:
                matrix[:, :, :, k] = 1
                restriction = Restriction(
                    coefficients=matrix,
                    sense=self.restriction_type.value,
                    resource=filtered_bands[0].band
                )
                restrictions.append(restriction)
        return restrictions

    def restrictions(self) -> list[Restriction]:
        return self.__restrictions

    @property
    def restriction_type(self) -> RestrictionType:
        return RestrictionType.LESS_OR_EQUAL
