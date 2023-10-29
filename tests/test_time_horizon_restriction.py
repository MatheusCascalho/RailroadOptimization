import numpy as np
from optimizer.restrictions.time_horizon_restriction import TimeHorizonRestriction
from optimizer.restrictions.railroad_elements import Node, Flow, TransitTime


def test_restriction_vector_for_one_origin_and_two_destinations_and_two_trains():
    n1 = Node(name='terminal 1', capacity=500)
    n2 = Node(name='terminal 2', capacity=600)
    n3 = Node(name='terminal 3', capacity=600)
    flows = [
        Flow(
            origin=n1,
            destination=n2,
            train_volume=50
        ),
        Flow(
            origin=n1,
            destination=n3,
            train_volume=60
        )
    ]
    transit_times = [
        TransitTime(origin=n1, destination=n2, time=20),
        TransitTime(origin=n1, destination=n3, time=30),
    ]
    constraint = TimeHorizonRestriction(trains=2, flows=flows, transit_times=transit_times, time_horizon=90)

    # Act
    actual = constraint.restrictions()[0].to_vector()

    # Assert
    expected = [
        40,      # t1->n2->n1->n2
        50,      # t1->n2->n1->n3
        50,      # t1->n3->n1->n2
        60,      # t1->n3->n1->n3
        40,      # t2->n2->n1->n2
        50,      # t2->n2->n1->n3
        50,      # t2->n3->n1->n2
        60,      # t2->n3->n1->n3
    ]
    expected = np.array(expected)

    np.testing.assert_allclose(actual, expected)
