from __future__ import absolute_import
from .. import abc
from collections import abc as abc_collection
import six


class AdjacencyGraph(abc.Graph):
    r"""
    Graph storing edge distances via adjacency lists

    :param source: adjacency information
    :param undirected: whether the graph enforces symmetry

    This graph provides optimal performance for random, direct access to nodes
    and edges. As it stores individual nodes and edges, it is optimal in both
    space and time for sparse graphs.

    However, ordering of :py:meth:`nodes`, :py:meth:`edges` and :py:meth:`values`
    is arbitrary. The expected complexity for searches is the worst case of O(len(:py:meth:`nodes`) = n)
    and O(len(:py:meth:`edges`) -> n\ :sup:`2`\ ), respectively.
    """
    def __init__(self, *source, undirected=False):
        self.undirected = undirected
        self._adjacency = {}  # {node: {neighbour: distance, neighbour: distance, ...}, ...}
        super(AdjacencyGraph, self).__init__(*source)
        if undirected:
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
        self._adjacency.update(self._adjacency_from_graph(graph))

    # initialize a new graph by copying nodes from an iterable
    def __init_iterable__(self, iterable, **kwargs):
        for node in iterable:
            self._adjacency.setdefault(node, {})

    # initialize a new graph by copying nodes, edges and values from a nested mapping
    def __init_mapping__(self, mapping, max_distance=None):
        self._adjacency.update(self._adjacency_from_mapping(mapping))

    def _ensure_symmetry(self):
        """
        Ensure that adjacency list is symmetric

        Adds any missing inverted edges. Raises :py:exc:`ValueError` if inverted edges do not have the same value.
        """
        adjacency = self._adjacency
        for node_a in adjacency:
            for node_b in adjacency[node_a]:
                try:
                    if adjacency[node_a][node_b] != adjacency[node_b][node_a]:
                        raise ValueError("symmetric graph initialized with asymmetric edges")
                except KeyError:
                    adjacency.setdefault(node_b, {})[node_a] = adjacency[node_a][node_b]

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
            elif value is None or value is item:
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

    def add(self, node):
        if node in self._adjacency:
            return
        self._adjacency[node] = {}

    def update(self, other):
        if isinstance(other, (abc.Graph, abc_collection.Mapping)):
            for node in other:
                try:
                    self._adjacency[node].update(other[node])
                except abc.NodeError:
                    self._adjacency[node] = dict(other[node])
        else:
            for node in other:
                self.add(node)

    def clear(self):
        for node in self:
            self._adjacency[node].clear()
