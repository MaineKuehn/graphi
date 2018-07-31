from __future__ import absolute_import
import collections as abc_collection

from .. import abc
from .. import edge
from .adjacency_graph import AdjacencyGraph


class UndirectedEdge(edge.Edge):
    """
    An undirected :py:term:`edge` as a pair of nodes

    For any :term:`nodes <node>` ``a`` and ``b``,
    the :py:class:`~.UndirectedEdge`\ s ``a:b`` and ``b:a`` are equivalent.
    As a result, which of the two is :py:attr:`~.UndirectedEdge.start` or :py:attr:`~.UndirectedEdge.stop`
    is arbitrary but well-defined.
    """
    def __init__(self, start, stop, step=None):
        # start and stop may be unsortable,
        # but the interface guarantees that they
        # are hashable
        if hash(start) > hash(stop):
            start, stop = stop, start
        super(UndirectedEdge, self).__init__(start, stop, step)

    def __eq__(self, other):
        if not isinstance(self, type(other)):
            return NotImplemented
        return {self.start, self.stop} == {other.start, other.stop}


class Undirected(abc.Graph):
    """
    Wrapper to make :py:class:`~.abc.Graph` instances undirected

    .. seealso::
        The :py:func:`undirectable` decorator for :py:class:`~.abc.Graph` classes.
    """
    @property
    def undirected(self):
        return True

    def __init__(self, *source, **kwargs):
        self._graph = AdjacencyGraph()
        super(Undirected, self).__init__(*source, **kwargs)
        assert kwargs.pop('undirected', True), "instances of class %s must be undirected" % self.__class__.__name__
        self._ensure_symmetry()

    # initialize a new graph by copying nodes, edges and values from another graph
    def __init_graph__(self, graph, **kwargs):
        # TODO: copy graph?
        self._graph = graph
        super(Undirected, self).__init_graph__(graph, **kwargs)

    # initialize a new graph by copying nodes from an iterable
    def __init_iterable__(self, iterable, **kwargs):
        self._graph.update(iterable)
        super(Undirected, self).__init_iterable__(iterable, **kwargs)

    # initialize a new graph by copying nodes, edges and values from a nested mapping
    def __init_mapping__(self, mapping, **kwargs):
        self._graph.update(mapping)
        super(Undirected, self).__init_mapping__(mapping, **kwargs)

    def _ensure_symmetry(self):
        """
        Ensure that all edges are symmetric

        Adds any missing inverted edges. Raises :py:exc:`ValueError` if inverted edges do not have the same value.
        """
        graph = self._graph
        graph_diff = {}
        for node_a in graph:
            adjacency = graph[node_a]
            for node_b in adjacency:
                try:
                    if adjacency[node_b] != graph[node_b:node_a]:
                        raise ValueError(
                            "symmetric graph initialized with asymmetric edge %s" % edge.Edge[node_a:node_b]
                        )
                except (abc.EdgeError, abc.NodeError):
                    graph_diff.setdefault(node_b, {})[node_a] = adjacency[node_b]
        if graph_diff:
            graph.update(graph_diff)

    def __getattr__(self, item):
        return getattr(self._graph, item)

    def __setattr__(self, key, value):
        if key != '_graph':
            setattr(self._graph, key, value)
        object.__setattr__(self, key, value)

    def __getitem__(self, item):
        return self._graph[item]

    def __setitem__(self, item, value):
        graph = self._graph
        if item.__class__ is slice:
            node_from, node_to = item.start, item.stop
            graph[node_from:node_to] = graph[node_to:node_from] = value
        else:
            # g[a] = {b: 3, c: 4, d: 6}
            if isinstance(value, abc_collection.Mapping):
                # if we know node already, clean up first
                if item in graph:
                    item_adjacency = list(graph[item])
                    for node_to in item_adjacency:
                        del graph[node_to:item]
                for node_to in value:
                    graph[node_to:item] = value[node_to]
            # always push on value here, to either finalise adjacency setting, default or raise
            graph[item] = value

    def __delitem__(self, item):
        graph = self._graph
        if isinstance(item, slice):
            node_from, node_to = item.start, item.stop
            del graph[node_from:node_to]
            del graph[node_to:node_from]
        else:
            # just remove `item`, `graph` has to remove
            # any incoming edges
            # while we *could* exploit being undirected
            # to remove incoming edges, we cannot tell
            # `graph` that we did so - it *has* to check
            # that all edges are gone either way
            del graph[item]

    def __iter__(self):
        return iter(self._graph)

    def __len__(self):
        return len(self._graph)

    def __bool__(self):
        return bool(self._graph)

    __nonzero__ = __bool__

    def __contains__(self, item):
        return item in self._graph

    def update(self, other):
        if isinstance(other, (abc.Graph, abc_collection.Mapping)):
            if not isinstance(other, Undirected):
                other = Undirected(other)
        self._graph.update(other)

    def clear(self):
        self._graph = type(self._graph)()

    # graph views
    def edges(self):
        """
        Return a new view of the graph's edges

        :return: view of the graph's edges
        :rtype: :py:class:`~.UndirectedEdgeView`
        """
        return UndirectedEdgeView(self)

    def values(self):
        """
        Return a new view of the values of the graph's edges

        :return: view of the values of the graph's edges
        :rtype: :py:class:`~.UndirectedValueView`
        """
        return UndirectedValueView(self)


class UndirectedEdgeView(abc.EdgeView):
    """
    View on the undirected edges in a graph
    """
    __slots__ = ()

    def __iter__(self):
        done_nodes = set()
        self_graph = self._graph
        for node_from in self_graph:
            for node_to in self_graph[node_from]:
                if node_to not in done_nodes:
                    yield UndirectedEdge(node_from, node_to)
            done_nodes.add(node_from)

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
        return sum(len(self_graph[node]) for node in self_graph) // 2


class UndirectedValueView(abc.ValueView):
    """
    View on the values of undirected edges in a graph
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
