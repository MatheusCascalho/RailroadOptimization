import numpy as np
from optimizer.restrictions.exchange_restriction import ExchangeRestriction
from optimizer.restrictions.railroad_elements import Node, Flow, ExchangeBand


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
    bands = [
        ExchangeBand(node=n2, band=50),
        ExchangeBand(node=n3, band=50),
    ]
    constraint = ExchangeRestriction(trains=2, flows=flows, bands=bands)

    # Act
    actual = constraint.restrictions()[0].to_vector()

    # Assert
    expected = [
        1,      # t1->n2->n1->n2
        0,      # t1->n2->n1->n3
        1,      # t1->n3->n1->n2
        0,      # t1->n3->n1->n3
        1,      # t2->n2->n1->n2
        0,      # t2->n2->n1->n3
        1,      # t2->n3->n1->n2
        0,      # t2->n3->n1->n3
    ]
    expected = np.array(expected)

    np.testing.assert_allclose(actual, expected)
