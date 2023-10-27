import numpy as np

from optimizer.restrictions.capacity_restriction import CapacityRestrictions, Node, Flow


def test_node_ids_should_follow_numeric_sequence_by_object_creation():
    n1 = Node(name='terminal 1', capacity=500)
    n2 = Node(name='terminal 2', capacity=600)
    assert n1.identifier == 0
    assert n2.identifier == 1


def test_restriction_matrix_for_one_flow_and_one_train():
    n1 = Node(name='terminal 1', capacity=500)
    n2 = Node(name='terminal 2', capacity=600)
    flow = Flow(
        origin=n1,
        destination=n2,
        train_volume=50
    )
    constraint = CapacityRestrictions(trains=1, flows=[flow])

    # Act
    actual = constraint.coefficients_matrix

    # Assert
    expected = [
        [
            50
        ]
    ]
    expected = np.array(expected)

    np.testing.assert_allclose(actual, expected)


def test_restriction_matrix_for_two_flows_and_one_train():
    n1 = Node(name='terminal 1', capacity=500)
    n2 = Node(name='terminal 2', capacity=600)
    flows = [
        Flow(
            origin=n1,
            destination=n2,
            train_volume=50
        ),
        Flow(
            origin=n2,
            destination=n1,
            train_volume=60
        )
    ]
    constraint = CapacityRestrictions(trains=1, flows=flows)

    # Act
    actual = constraint.coefficients_matrix

    # Assert
    expected = [
        [  # constraints for origin j0
            0,  # t1->n1->n1->n1
            50,  # t1->n1->n1->n2
            0,  # t1->n1->n2->n1
            0,  # t1->n1->n2->n2
            0,  # t1->n2->n1->n1
            50,  # t1->n2->n1->n2
            0,  # t1->n2->n2->n1
            0  # t1->n2->n2->n2
        ],
        [  # constraints for origin j1
            0,  # t1->n1->n1->n1
            0,  # t1->n1->n1->n2
            60,  # t1->n1->n2->n1
            0,  # t1->n1->n2->n2
            0,  # t1->n2->n1->n1
            0,  # t1->n2->n1->n2
            60,  # t1->n2->n2->n1
            0  # t1->n2->n2->n2
        ],
    ]
    expected = np.array(expected)

    np.testing.assert_allclose(actual, expected)


def test_restriction_vector_for_two_flows_and_one_train():
    n1 = Node(name='terminal 1', capacity=500)
    n2 = Node(name='terminal 2', capacity=600)
    flows = [
        Flow(
            origin=n1,
            destination=n2,
            train_volume=50
        ),
        Flow(
            origin=n2,
            destination=n1,
            train_volume=60
        )
    ]
    constraint = CapacityRestrictions(trains=1, flows=flows)

    # Act
    actual = constraint.restrictions()[0].to_vector()

    # Assert
    expected = [
        0,      # t1->n1->n1->n1
        50,     # t1->n1->n1->n2
        0,      # t1->n1->n2->n1
        0,      # t1->n1->n2->n2
        0,      # t1->n2->n1->n1
        50,     # t1->n2->n1->n2
        0,      # t1->n2->n2->n1
        0       # t1->n2->n2->n2
    ]
    expected = np.array(expected)

    np.testing.assert_allclose(actual, expected)