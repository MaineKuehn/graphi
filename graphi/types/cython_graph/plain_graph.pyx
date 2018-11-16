# cython: language_level=3
from __future__ import absolute_import
import collections as abc_collection
from itertools import islice

from graphi.abc import Graph as GraphABC, EdgeError, NodeError, AdjacencyListTypeError, \
    NodeView as NodeViewABC, EdgeView as EdgeViewABC, ValueView as ValueViewABC, ItemView as ItemViewABC
from graphi.edge import Edge


Graph_or_Map = (GraphABC, abc_collection.Mapping)


cdef class CythonGraph(object):
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
    #: node -> {neighbour_1, neighbour_2, neighbour_3, ...}
    cdef dict _incidences
    #: node, node -> value
    cdef dict _edge_values

    def __init__(self, *source, **kwargs):
        self._incidences = {}  # {node: {neighbour, neighbour, ...}}
        self._edge_values = {}  # {(node, node): value, (node, node): value, ...}
        if not source:
            self.__init_empty__(**kwargs)
        elif len(source) == 1 and isinstance(source[0], GraphABC):
            self.__init_graph__(source[0], **kwargs)
        elif len(source) == 1 and isinstance(source[0], abc_collection.Mapping):
            self.__init_mapping__(source[0], **kwargs)
        elif len(source) == 1 and isinstance(source[0], abc_collection.Iterable):
            self.__init_iterable__(source[0], **kwargs)
        else:
            self.__init_iterable__(source, **kwargs)

    def _adjacency_from_graph(self, graph):
        adjacency = {}
        for node in graph:
            adjacency[node] = {other: graph[node:other] for other in graph[node]}
        return adjacency

    def _adjacency_from_mapping(self, adjacency_dict):
        adjacency = {}
        for node, neighbours in adjacency_dict.items():
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
            self._incidences[node] = set()
        self.__init_kwargs__(**kwargs)

    # initialize a new graph by copying nodes, edges and values from a nested mapping
    def __init_mapping__(self, mapping, **kwargs):
        self.update(self._adjacency_from_mapping(mapping))
        self.__init_kwargs__(**kwargs)

    # raise for any non-digested keyword arguments
    def __init_kwargs__(self, **kwargs):
        if kwargs:
            if len(kwargs) > 1:
                raise TypeError(
                    '%r are invalid keyword arguments for %s' % (
                        ', '.join(kwargs), self.__class__.__name__
                    ))
            raise TypeError('%r is an invalid keyword argument for %s' % (
                next(iter(kwargs)), self.__class__.__name__)
            )

    def __getitem__(self, item):
        if item.__class__ is slice:
            node_from, node_to = item.start, item.stop
            try:
                return self._edge_values[node_from, node_to]
            except KeyError:
                raise EdgeError(item)
        else:
            if item in self._incidences:
                return NodeAdjacencyView(self, item)
            else:
                raise NodeError(item)

    def __setitem__(self, item, value):
        if item.__class__ is slice:
            node_from, node_to = item.start, item.stop
            if node_from not in self._incidences:
                raise NodeError(node_from)  # first edge node
            elif node_to not in self._incidences:
                raise NodeError(node_to)  # second edge node
            self._set_edge(node_from, node_to, value)
        else:
            # g[a] = g[a]
            if isinstance(value, NodeAdjacencyView):
                if value._graph is self and value._node_from is item:
                    return
                raise NotImplementedError('cannot digest NodeAdjacencyViews')
            # g[a] = True
            elif value is True:
                self._add_node(item)
            # g[a] = {b: 3, c: 4, d: 6}
            elif isinstance(value, abc_collection.Mapping):
                self._add_node(item)
                for node_to in value:
                    self._add_node(node_to)
                    self._set_edge(item, node_to, value[node_to])
            else:
                raise AdjacencyListTypeError(value)

    def __delitem__(self, item):
        if isinstance(item, slice):
            node_from, node_to = item.start, item.stop
            try:
                del self._edge_values[node_from, node_to]
            except KeyError:
                raise EdgeError(item)
            else:
                self._incidences[node_from].remove(node_to)
        else:
            try:
                incidences = self._incidences.pop(item)
            except KeyError:
                raise NodeError(item)
            else:
                for node_to in incidences:
                    del self._edge_values[item, node_to]
                for node_from in self:
                    try:
                        del self._edge_values[node_from, item]
                    except KeyError:
                        pass

    def __iter__(self):
        return iter(self._incidences)

    def __len__(self):
        return len(self._incidences)

    def __bool__(self):
        return bool(self._incidences)

    def __nonzero__(self):
        return bool(self._incidences)

    def __contains__(self, item):
        if item.__class__ is slice:
            node_from, node_to = item.start, item.stop
            return (node_from, node_to) in self._edge_values
        else:
            return item in self._incidences

    def clear(self):
        self._incidences = {}
        self._edge_values = {}

    def copy(self):
        return CythonGraph(self)

    def nodes(self):
        return NodeView(self)

    def edges(self):
        return EdgeView(self)

    def values(self):
        return ValueView(self)

    def items(self):
        return ItemView(self)

    cpdef add(self, item):
        # Cython makes practically the same C code for real and faked slices
        # no need to distinguish between them
        if item.__class__ is slice:
            node_from, node_to = item.start, item.stop
            self._add_node(node_from)
            self._add_node(node_to)
            self._add_edge(node_from, node_to)
        else:
            self._add_node(item)

    def discard(self, item):
        try:
            del self[item]
        except (NodeError, EdgeError):
            pass

    cpdef update(self, other):
        if isinstance(other, Graph_or_Map):
            for node_from in other:
                self._add_node(node_from)
                node_adjacency = other[node_from]
                for node_to in node_adjacency:
                    self._add_node(node_to)
                    self._set_edge(node_from, node_to, node_adjacency[node_to])
        else:
            for node in other:
                self._add_node(node)

    def get(self, item, default=None):
        if item.__class__ is slice:
            node_from, node_to = item.start, item.stop
            try:
                return self._edge_values[node_from, node_to]
            except KeyError:
                return default
        else:
            if item in self._incidences:
                return NodeAdjacencyView(self, item)
            else:
                return default

    # pure Cython helper methods
    ############################
    cdef _add_node(self, node):
        """Ensure that `node` is part of self"""
        if node not in self._incidences:
            self._incidences[node] = set()

    cdef _add_edge(self, node_from, node_to):
        """Ensure that node_from:node_to is part of self; does not _add either node"""
        cdef set incidence
        if (node_from, node_to) not in self._edge_values:
            incidence = self._incidences[node_from]
            incidence.add(node_to)
            self._edge_values[node_from, node_to] = True

    cdef _set_edge(self, node_from, node_to, value):
        """Ensure that node_from:node_to is set to value; does not _add either node"""
        cdef set incidence = self._incidences[node_from]
        incidence.add(node_to)
        self._edge_values[node_from, node_to] = value

    # representations
    #################
    cdef str _data_str(self):
        return '{%s}' % ', '.join(NodeAdjacencyView(self, node)._data_str() for node in self)

    def __str__(self):
        if len(self._incidences) <= 16:
            return '%s(%s)' % (self.__class__.__name__, self._data_str())
        elif len(self._incidences) <= 64:
            incidences = list(self._incidences)
            return '%s({%s, %s})' % (
                self.__class__.__name__,
                ', '.join(NodeAdjacencyView(node)._data_str() for node in incidences[:16]),
                ', '.join('%r: {...}' % node for node in incidences[16:]),
            )
        elif len(self._incidences) <= 128:
            return '%s({%s})' % (
                self.__class__.__name__,
                ', '.join('%r: {...}' % node for node in self._incidences),
            )
        else:
            return '%s({%s, ...})' % (
                self.__class__.__name__,
                ', '.join('%r: {...}' % node for node in islice(self._incidences, 128)),
            )

    def __repr__(self):
        return '<%s of %d nodes, %d edges at %s>' % (
            self.__class__.__name__, len(self._incidences), len(self._edge_values), id(self))


# View Objects
# These directly access the data of a CythonGraph

cdef class NodeAdjacencyView(object):
    """View to the Adjacency of a Node"""
    cdef CythonGraph _graph
    cdef object _node_from

    def __init__(self, CythonGraph graph, object node_from):
        self._graph = graph
        self._node_from = node_from

    def __getitem__(self, node):
        return self._graph[self._node_from:node]

    def __iter__(self):
        return iter(self._graph._incidences[self._node_from])

    def __len__(self):
        return len(self._graph._incidences[self._node_from])

    def __contains__(self, node):
        return (self._node_from, node) in self._graph._edge_values

    cdef str _data_str(self):
        return '%r : {%s}' % (
            self._node_from,
            ', '.join('%r: %r' % (node_to, self._graph[self._node_from:node_to])
            for node_to in self._graph._incidences[self._node_from])
        )

    def __str__(self):
        return '<%s>' % self._data_str()

    def __repr__(self):
        return '<%s of %r in %r>' % (self.__class__.__name__, self._node_from, self._graph)


cdef class NodeView(object):
    """
    View on the nodes of a graph
    """
    cdef CythonGraph _graph

    def __init__(self, CythonGraph graph):
        self._graph = graph

    def __iter__(self):
        return iter(self._graph._incidences)

    def __contains__(self, node):
        return node in self._graph._incidences

    def __len__(self):
        return len(self._graph._incidences)

    cdef str _data_str(self):
        return '%s' % (
            ','.join(repr(node) for node in self)
        )

    def __str__(self):
        return '<%s>' % self._data_str()

    def __repr__(self):
        return '<%s of %r>' % (self.__class__.__name__, self._graph)


cdef class EdgeView(object):
    """View on the edges in a graph"""
    cdef CythonGraph _graph

    def __init__(self, CythonGraph graph):
        self._graph = graph

    def __iter__(self):
        for node_from, node_to in self._graph._edge_values:
            yield Edge(node_from, node_to)

    def __contains__(self, pair):
        if pair.__class__ is slice:
            return pair in self._graph
        else:
            try:
                node_from, node_to = pair
            except ValueError:
                pass
            else:
                return (node_from, node_to) in self._graph._edge_values
        raise TypeError('an edge or pair is required')

    def __len__(self):
        return len(self._graph._edge_values)

    cdef str _data_str(self):
        return '%s' % (
            ','.join(repr(edge) for edge in self)
        )

    def __str__(self):
        return '<%s>' % self._data_str()

    def __repr__(self):
        return '<%s of %r>' % (self.__class__.__name__, self._graph)


cdef class ValueView(object):
    """
    View on the values of edges in a graph
    """
    cdef CythonGraph _graph

    def __init__(self, CythonGraph graph):
        self._graph = graph

    def __iter__(self):
        return iter(self._graph._edge_values.values())

    def __contains__(self, value):
        return any(edge_value == value for edge_value in iter(self))

    def __len__(self):
        return len(self._graph._edge_values)

    cdef str _data_str(self):
        return '%s' % (
            ','.join(repr(value) for value in self)
        )

    def __str__(self):
        return '<%s>' % self._data_str()

    def __repr__(self):
        return '<%s of %r>' % (self.__class__.__name__, self._graph)


cdef class ItemView(object):
    """
    View on the edges and values in a graph

    Represents edges and their value as a :py:class:`tuple` of ``(tail, head, value)``.
    For example, the edge ``graph[a:b] = c`` corresponds to the item ``(a, b, c)``.
    """
    cdef CythonGraph _graph

    def __init__(self, CythonGraph graph):
        self._graph = graph

    def __iter__(self):
        for edge, value in self._graph._edge_values.items():
            node_from, node_to = edge
            yield node_from, node_to, value

    def __contains__(self, edge_value):
        try:
            node_a, node_b, value = edge_value
        except ValueError:
            raise TypeError('items must be of length 3')
        try:
            return self._graph._edge_values[node_a, node_b] == value
        except KeyError:
            return False

    def __len__(self):
        return len(self._graph._edge_values)

    cdef str _data_str(self):
        return '%s' % (
            ','.join(repr(items) for items in self)
        )

    def __str__(self):
        return '<%s>' % self._data_str()

    def __repr__(self):
        return '<%s of %r>' % (self.__class__.__name__, self._graph)


GraphABC.register(CythonGraph)
EdgeViewABC.register(EdgeView)
ValueViewABC.register(ValueView)
ItemViewABC.register(ItemView)
NodeViewABC.register(NodeView)
