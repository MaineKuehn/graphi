from __future__ import absolute_import
from .. import abc
from collections import abc as abc_collection
import six


class AdjacencyListTypeError(TypeError):
    """AdjacencyList was set to incorrect type"""
    def __init__(self, edge):
        TypeError.__init__("AdjacencyList must be None, its node or a mapping, not %r" %
                           edge.__class__)


class AdjacencyGraph(abc.Graph):
    """
    Graph storing edge distances via adjacency lists.

    :param source: adjacency information
    :param undirected: whether the graph enforces symmetry
    """
    def __init__(self, source=None, undirected=False, max_distance=None):
        self.undirected = undirected
        self._adjacency = {}  # {node: {neighbour: distance, neighbour: distance, ...}, ...}
        # TODO: handle different possible sources
        if isinstance(source, abc_collection.Mapping):
            self._adjacency.update(self._adjacency_from_mapping(source, max_distance))

    @staticmethod
    def _adjacency_from_mapping(adjacency_dict, max_distance):
        adjacency = {}
        for node, neighbours in six.viewitems(adjacency_dict):
            if not max_distance:
                adjacency[node] = {other: neighbours[other] for other in neighbours}
            else:
                adjacency[node] = {
                    other: neighbours[other] for other in neighbours if neighbours[other] <= max_distance
                }
        return adjacency

    def __getitem__(self, item):
        if isinstance(item, slice):
            assert item.step is None, "%s does not support stride argument for edges" % \
                                      self.__class__.__name__
            node_from, node_to = item.start, item.stop
            try:
                return self._adjacency[node_from][node_to]
            except KeyError:
                raise abc.NoSuchEdge
        else:
            try:
                return self._adjacency[item]
            except KeyError:
                raise abc.NoSuchNode

    def __setitem__(self, item, value):
        if isinstance(item, slice):
            node_from, node_to = item.start, item.stop
            if node_to not in self._adjacency:
                raise abc.NoSuchNode  # second edge node
            try:
                self._adjacency[node_from][node_to] = value
                if self.undirected:
                    self._adjacency[node_to][node_from] = value
            except KeyError:
                raise abc.NoSuchNode  # first edge node
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
                self._adjacency[item] = value.copy()
            else:
                raise AdjacencyListTypeError(value)

    def __delitem__(self, item):
        if isinstance(item, slice):
            node_from, node_to = item.start, item.stop
            try:
                del self._adjacency[node_from][node_to]
                if self.undirected:
                    del self._adjacency[node_to][node_from]
            except KeyError:
                raise abc.NoSuchEdge
        else:
            try:
                node_adjacency = self._adjacency.pop(item)
            except KeyError:
                raise abc.NoSuchNode
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

    def neighbourhood(self, node, distance=None):
        try:
            adjacency_list = self._adjacency[node]
        except KeyError:
            raise abc.NoSuchNode
        else:
            if not distance:
                return iter(adjacency_list)
            return (neighbour for neighbour in adjacency_list if adjacency_list[neighbour] <= distance)
