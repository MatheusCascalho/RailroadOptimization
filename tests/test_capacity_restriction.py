from optimizer.restrictions.capacity_restriction import CapacityRestrictions, Node, Flow


def test_node_ids_should_follow_numeric_sequence_by_object_creation():
    n1 = Node(name='terminal 1', capacity=500)
    n2 = Node(name='terminal 2', capacity=600)
    assert n1.identifier == 0
    assert n2.identifier == 1
