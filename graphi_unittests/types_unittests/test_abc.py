import six
import collections as abc_collection
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from graphi.abc import Graph, EdgeError, NodeError, AdjacencyListTypeError

from . import _graph_interface_mixins as mixins


class SimpleGraph(Graph):
    """Test Graph using the entire ABC base functionality"""
    def __init__(self, *source, **kwargs):
        self._adjacency = {}  # {node: {neighbour: distance, neighbour: distance, ...}, ...}
        super(SimpleGraph, self).__init__(*source, **kwargs)

    @staticmethod
    def _adjacency_from_graph(graph):
        adjacency = {}
        for node in graph:
            adjacency[node] = {other: graph[node:other] for other in graph[node]}
        return adjacency

    @staticmethod
    def _adjacency_from_mapping(adjacency_dict):
        adjacency = {}
        for node, neighbours in six.viewitems(adjacency_dict):
            adjacency[node] = {other: neighbours[other] for other in neighbours}
        return adjacency

    def __init_empty__(self, **kwargs):
        self.__init_kwargs__(**kwargs)

    # initialize a new graph by copying nodes, edges and values from another graph
    def __init_graph__(self, graph, **kwargs):
        self.update(self._adjacency_from_graph(graph))
        self.__init_kwargs__(**kwargs)

    # initialize a new graph by copying nodes from an iterable
    def __init_iterable__(self, iterable, **kwargs):
        for node in iterable:
            self._adjacency.setdefault(node, {})
        self.__init_kwargs__(**kwargs)

    # initialize a new graph by copying nodes, edges and values from a nested mapping
    def __init_mapping__(self, mapping, **kwargs):
        self.update(self._adjacency_from_mapping(mapping))
        self.__init_kwargs__(**kwargs)

    def __getitem__(self, item):
        if item.__class__ is slice:
            node_from, node_to = item.start, item.stop
            try:
                return self._adjacency[node_from][node_to]
            except KeyError:
                raise EdgeError
        else:
            try:
                return self._adjacency[item]
            except KeyError:
                raise NodeError

    def __setitem__(self, item, value):
        if item.__class__ is slice:
            node_from, node_to = item.start, item.stop
            try:
                self._adjacency[node_from][node_to] = value
            except KeyError:
                raise NodeError  # first or second edge node
        else:
            # g[a] = g[a]
            if self._adjacency.get(item, object()) is value:
                return
            # g[a] = True
            elif value is True:
                if item not in self._adjacency:
                    self._adjacency[item] = {}
            # g[a] = {b: 3, c: 4, d: 6}
            elif isinstance(value, abc_collection.Mapping):
                self._adjacency[item] = dict(value)
            else:
                raise AdjacencyListTypeError(value)

    def __delitem__(self, item):
        if isinstance(item, slice):
            node_from, node_to = item.start, item.stop
            try:
                del self._adjacency[node_from][node_to]
            except KeyError:
                raise EdgeError
        else:
            try:
                self._adjacency.pop(item)
            except KeyError:
                raise NodeError
            else:
                for node in self:
                    self._adjacency[node].pop(item, None)

    def __iter__(self):
        return iter(self._adjacency)

    def clear(self):
        self._adjacency = type(self._adjacency)()


class TestAdjacencyGraphInterface(mixins.Mixin.GraphInitMixin, mixins.Mixin.GraphInterfaceMixin):
    graph_cls = SimpleGraph
