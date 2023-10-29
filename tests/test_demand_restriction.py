import numpy as np
from optimizer.restrictions.demand_restriction import MaximumDemandRestriction, MinimumDemandRestriction
from optimizer.restrictions.railroad_elements import Node, Flow, Demand


def test_demand_restriction_vector_for_one_origin_and_two_destinations_and_two_trains():
    n1 = Node(name='terminal 1', capacity=500)
    n2 = Node(name='terminal 2', capacity=600)
    n3 = Node(name='terminal 3', capacity=600)
    f1 = Flow(
        origin=n1,
        destination=n2,
        train_volume=50
    )
    f2 = Flow(
        origin=n1,
        destination=n3,
        train_volume=60
    )

    demands = [
        Demand(flow=f1, minimum=30e3, maximum=50e3),
        Demand(flow=f2, minimum=20e3, maximum=40e3),
    ]

    constraint = MaximumDemandRestriction(trains=2, demands=demands)

    # Act
    actual = constraint.restrictions()[0].to_vector()

    # Assert
    expected = [
        50,      # t1->n2->n1->n2
        0,       # t1->n2->n1->n3
        50,      # t1->n3->n1->n2
        0,       # t1->n3->n1->n3
        50,      # t2->n2->n1->n2
        0,       # t2->n2->n1->n3
        50,      # t2->n3->n1->n2
        0,       # t2->n3->n1->n3
    ]
    expected = np.array(expected)

    np.testing.assert_allclose(actual, expected)


def test_maximum_demand_resource_vector_for_one_origin_and_two_destinations_and_two_trains():
    n1 = Node(name='terminal 1', capacity=500)
    n2 = Node(name='terminal 2', capacity=600)
    n3 = Node(name='terminal 3', capacity=600)
    f1 = Flow(
        origin=n1,
        destination=n2,
        train_volume=50
    )
    f2 = Flow(
        origin=n1,
        destination=n3,
        train_volume=60
    )

    demands = [
        Demand(flow=f1, minimum=30e3, maximum=50e3),
        Demand(flow=f2, minimum=20e3, maximum=40e3),
    ]

    constraint = MaximumDemandRestriction(trains=2, demands=demands)

    # Act
    actual = constraint.resource_vector

    # Assert
    expected = [
        50e3,
        40e3,
    ]
    expected = np.array(expected)

    np.testing.assert_allclose(actual, expected)


def test_minimum_demand_resource_vector_for_one_origin_and_two_destinations_and_two_trains():
    n1 = Node(name='terminal 1', capacity=500)
    n2 = Node(name='terminal 2', capacity=600)
    n3 = Node(name='terminal 3', capacity=600)
    f1 = Flow(
        origin=n1,
        destination=n2,
        train_volume=50
    )
    f2 = Flow(
        origin=n1,
        destination=n3,
        train_volume=60
    )

    demands = [
        Demand(flow=f1, minimum=30e3, maximum=50e3),
        Demand(flow=f2, minimum=20e3, maximum=40e3),
    ]

    constraint = MinimumDemandRestriction(trains=2, demands=demands)

    # Act
    actual = constraint.resource_vector

    # Assert
    expected = [
        30e3,
        20e3,
    ]
    expected = np.array(expected)

    np.testing.assert_allclose(actual, expected)
