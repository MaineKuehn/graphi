try:
    from singledispatch import singledispatch
except ImportError:
    from functools import singledispatch


@singledispatch
def neighbours(graph, node, maximum_distance=None):
    """
    Yield all nodes to which there is an outgoing edge from ``node`` in ``graph``

    :param graph: graph in which to search for edges
    :type graph: :py:class:`~graphi.abc.Graph`
    :param node: node from which edges originate.
    :param maximum_distance: maximum distance to other nodes
    :return: iterator of neighbour nodes
    :raises NodeError: if ``node`` is not in the graph

    When ``maximum_distance`` is not :py:const:`None`, it is the maximum allowed edge value.
    This is interpreted using the ``<=`` operator as ``graph[edge] <= distance``.

    If there is a valid edge ``graph[node:node] <= distance``, then ``node``
    is part of its own neighbourhood.

    :note: The order of neighbours is arbitrary.
    """
    adjacency = graph[node]
    if maximum_distance is None:
        return iter(adjacency)
    return (neighbour for neighbour in adjacency if adjacency[neighbour] <= maximum_distance)
