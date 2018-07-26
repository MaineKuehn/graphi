from __future__ import absolute_import
import collections as abc_collection
import six

from .. import abc
from .. import edge


class AdjacencyGraph(abc.Graph):
    r"""
    Graph storing edge distances via adjacency lists

    :param source: adjacency information
    :param undirected: whether the graph enforces symmetry

    This graph provides optimal performance for random, direct access to nodes
    and edges. As it stores individual nodes and edges, it is optimal in both
    space and time for sparse graphs.

    However, ordering of :py:meth:`nodes`, :py:meth:`edges` and :py:meth:`values`
    is arbitrary. The expected complexity for searches is the worst case of
    O(len(:py:meth:`nodes`) = n) and O(len(:py:meth:`edges`) -> n\ :sup:`2`\ ),
    respectively.
    """
    def __init__(self, *source, **kwargs):
        self.undirected = kwargs.pop('undirected', False)
        self._adjacency = {}  # {node: {neighbour: distance, neighbour: distance, ...}, ...}
        super(AdjacencyGraph, self).__init__(*source)
        if self.undirected:
            self._ensure_symmetry()

    @staticmethod
    def _adjacency_from_graph(graph):
        adjacency = {}
        for node in graph:
            adjacency[node] = {other: graph[node:other] for other in graph}
        return adjacency

    @staticmethod
    def _adjacency_from_mapping(adjacency_dict):
        adjacency = {}
        for node, neighbours in six.viewitems(adjacency_dict):
            adjacency[node] = {other: neighbours[other] for other in neighbours}
        return adjacency

    def __init_empty__(self, max_distance=None):
        return

    # initialize a new graph by copying nodes, edges and values from another graph
    def __init_graph__(self, graph, max_distance=None):
        self.update(self._adjacency_from_graph(graph))

    # initialize a new graph by copying nodes from an iterable
    def __init_iterable__(self, iterable, **kwargs):
        for node in iterable:
            self._adjacency.setdefault(node, {})

    # initialize a new graph by copying nodes, edges and values from a nested mapping
    def __init_mapping__(self, mapping, max_distance=None):
        self.update(self._adjacency_from_mapping(mapping))

    def _ensure_symmetry(self):
        """
        Ensure that adjacency list is symmetric

        Adds any missing inverted edges. Raises :py:exc:`ValueError` if inverted edges do not have the same value.
        """
        adjacency = self._adjacency
        adjacency_diff = {}
        for node_a in adjacency:
            for node_b in adjacency[node_a]:
                try:
                    if adjacency[node_a][node_b] != adjacency[node_b][node_a]:
                        raise ValueError("symmetric graph initialized with asymmetric edges")
                except KeyError:
                    adjacency_diff.setdefault(node_b, {})[node_a] = adjacency[node_a][node_b]
        adjacency.update(adjacency_diff)

    def __getitem__(self, item):
        if item.__class__ is slice:
            node_from, node_to = item.start, item.stop
            try:
                return self._adjacency[node_from][node_to]
            except KeyError:
                raise abc.EdgeError
        else:
            try:
                return self._adjacency[item]
            except KeyError:
                raise abc.NodeError

    def __setitem__(self, item, value):
        if item.__class__ is slice:
            node_from, node_to = item.start, item.stop
            if node_to not in self._adjacency:
                raise abc.NodeError  # second edge node
            try:
                self._adjacency[node_from][node_to] = value
                if self.undirected:
                    self._adjacency[node_to][node_from] = value
            except KeyError:
                raise abc.NodeError  # first edge node
        else:
            # g[a] = g[a]
            if self._adjacency.get(item, object()) is value:
                return
            # g[a] = None, g[a] = a
            elif value is True:
                if item not in self._adjacency:
                    self._adjacency[item] = {}
            # g[a] = {b: 3, c: 4, d: 6}
            elif isinstance(value, abc_collection.Mapping):
                if self.undirected:
                    # if we know node already, clean up first
                    if item in self._adjacency:
                        for node_to in self._adjacency[item]:
                            del self._adjacency[node_to][item]  # safe unless graph not undirected
                    for node_to in value:
                        self._adjacency[node_to][item] = value[node_to]
                self._adjacency[item] = dict(value)
            else:
                raise abc.AdjacencyListTypeError(value)

    def __delitem__(self, item):
        if isinstance(item, slice):
            node_from, node_to = item.start, item.stop
            try:
                del self._adjacency[node_from][node_to]
                if self.undirected:
                    del self._adjacency[node_to][node_from]
            except KeyError:
                raise abc.EdgeError
        else:
            try:
                node_adjacency = self._adjacency.pop(item)
            except KeyError:
                raise abc.NodeError
            else:
                # clean up all edges to this node
                if self.undirected:
                    for node in node_adjacency:
                        del self._adjacency[node][item]  # safe unless graph not undirected
                else:
                    for node in self:
                        self._adjacency[node].pop(item, None)

    def __iter__(self):
        return iter(self._adjacency)

    def __len__(self):
        return len(self._adjacency)

    def __bool__(self):
        return bool(self._adjacency)

    __nonzero__ = __bool__

    def __contains__(self, item):
        if item.__class__ is slice:
            node_from, node_to = item.start, item.stop
            try:
                return node_to in self._adjacency[node_from]
            except KeyError:
                return False
        else:
            return item in self._adjacency

    def update(self, other):
        if isinstance(other, (abc.Graph, abc_collection.Mapping)):
            for node in other:
                try:
                    self._adjacency[node].update(other[node])
                except KeyError:
                    self._adjacency[node] = dict(other[node])
        else:
            for node in other:
                self.add(node)

    def clear(self):
        for node in self:
            self._adjacency[node].clear()

    def edges(self):
        return EdgeView(self)

    def values(self):
        return ValueView(self)


class EdgeView(abc.EdgeView):
    """
    View on the edges in a graph
    """
    __slots__ = ()

    def __iter__(self):
        self_graph = self._graph
        for node_from in self_graph:
            for node_to in self_graph[node_from]:
                yield edge.Edge(node_from, node_to)

    def __contains__(self, pair):
        if pair.__class__ is slice:
            return pair in self._graph
        else:
            try:
                return edge.Edge(*pair) in self._graph
            except TypeError:
                pass
        raise TypeError('an edge is required')

    def __len__(self):
        self_graph = self._graph
        return sum(len(self_graph[node]) for node in self_graph)


class ValueView(abc.ValueView):
    """
    View on the values of edges in a graph
    """
    __slots__ = ()

    def __iter__(self):
        self_graph = self._graph
        for _edge in self_graph.edges():
            yield self_graph[_edge]

    def __contains__(self, value):
        self_graph = self._graph
        return any(self_graph[_edge] == value for _edge in self_graph.edges())

    def __len__(self):
        return len(self._graph.edges())
