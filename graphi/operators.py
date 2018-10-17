from __future__ import division

try:
    from singledispatch import singledispatch
except ImportError:
    from functools import singledispatch


@singledispatch
def density(graph):
    """
    Return the density of the graph, i.e. the connectedness of its nodes

    :param graph: graph for which to calculate density
    :type graph: :py:class:`~graphi.abc.Graph`
    :raises ValueError: if ``graph`` has no nodes

    The density is the ratio of actual edge count versus the maximum, non-looping edge count.

    A graph without edges has a density of ``0``, whereas a complete graph has a density of ``1``.
    A graph with a :term:`loop` may have a density bigger than ``1``.
    The density is undefined for a graph less than two nodes, and raises :py:exc:`ValueError`.
    """
    if not graph:
        raise ValueError
    node_count = len(graph)
    if node_count <= 1:
        raise ValueError
    edge_count = len(graph.edges())
    return edge_count / (node_count * (node_count - 1))


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
