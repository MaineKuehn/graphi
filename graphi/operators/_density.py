from __future__ import division
from . import interface


@interface.graph_operator
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
