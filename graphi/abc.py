from __future__ import absolute_import

import abc
import itertools
try:
    from collections import abc as abc_collection
except ImportError:
    import collections as abc_collection

from . import edge


class EdgeError(Exception):
    """Graph edge not found"""
    pass


class NodeError(Exception):
    """Graph node not found"""
    pass


class AdjacencyListTypeError(TypeError):
    """AdjacencyList set with an incorrect type"""
    def __init__(self, item):
        TypeError.__init__(self, 'AdjacencyList of a node must be True or a mapping, not %r' % item.__class__.__name__)


class Graph(abc_collection.Container):
    """
    Abstract Base Class for graphs representing values of edges between nodes

    A :py:class:`~.Graph` is a container for primitive nodes and edges.
    There are three types of elements handled by a graph:

    1. primitive *nodes*,

    2. slice-like *edges* as pairs of nodes, and

    3. primitive *edge values*.

    Both nodes and edge values are conceptually similar to keys and values of :py:class:`dict`.
    However, the concept of node pairs as edges adds additional functionality.
    The fixed relation between arbitrary nodes ``a, b`` and the directed pair ``a:b`` creates two value-type layers:

    1. each *node* is mapped to all its outgoing edges,

    2. each *edge* is mapped to the respective edge value.

    In short, ``graph[a]`` provides a collection of edges originating at ``a``,
    while ``graph[a:b]`` provides the specific edge value from ``a`` to ``b``.

    .. note:: Many interfaces return the rich :py:class:`~.Edge` type for its added usability.
              To access an edge value, using :py:class:`slice` such as ``graph[a:b]`` is sufficient, however.

    Similar to :py:class:`Mappings`, nodes are the primary keys of a :py:class:`~.Graph`.
    As a result, the container interfaces, such as ``iter`` and ``len``, operate on nodes.
    In general, nodes can be of arbitrary type as long as they are :term:`hashable`.

    By default, edges in a :py:class:`~.Graph` are directed and unique:
    The edges represented by ``graph[a:b]`` and ``graph[b:a]`` are separate with opposite direction.
    Each edge is unique, i.e. there is only one edge ``graph[a:b]``.
    A loop is represented by the edge ``graph[a:a]``.
    The edge entities stored in the graph may be arbitrary objects.

    As such, the interface of :py:class:`~.Graph` defaults to describing a directed graph.
    However, other types of graph can be expressed as well.
    These generally do not form separate types in term of implementation.

    **Multigraphs** allow for multiple edges between pairs of nodes.
    In this case, all edge values are containers (such as :py:class:`list` or :py:class:`set`) of arbitrary size.
    Whether a :py:class:`~.Graph` is a graph of containers or a multigraph depends on the context.

    **Undirected Graphs** do not distinguish between ``graph[a:b]`` and ``graph[b:a]``.
    This can be enforced by symmetry of edge values, which guarantees that ``graph[a:b] == graph[b:a]`` always applies.

    .. describe:: g.undirected

      Indicates whether :py:class:`~.Graph` ``g`` is guaranteed to be undirected, having only
      symmetric edge values. If :py:const:`True`, ``g[a:b] is g[b:a]`` for any nodes ``a`` and ``b``
      in ``g``; the graph enforces this, e.g. ``g[a:b] = c`` implies ``g[b:a] = c``.
      If :py:const:`False`, symmetric edges are allowed but not enforced.

      Read-only unless explicitly indicated otherwise.

    There are several ways to initialise a new graph;
    their main difference is which element types are left empty.

    .. describe:: Graph()

      Create a new empty graph.
      No nodes, edges or values are filled in.

    .. describe:: Graph(graph)

      Create a new graph with all nodes, edges and values of ``graph``.
      The resulting graph is a shallow copy of ``graph`` - the identity of elements is preserved.

    .. describe:: Graph(a, b, c, ...)
                  Graph([a, b, c, ...])
                  Graph({a, b, c, ...})
                  Graph(<iterable for a, b, c, ...>)

      Create a new graph with nodes ``a``, ``b``, ``c``, ``d``, and so on.
      No edges or values are created explicitly.

    .. describe:: Graph({a: {b: ab_edge, c: ...}, b: {a: ab_edge, ...}})
                  Graph({a: AdjacencyList({b: ab_edge, c: ...}), b: AdjacencyList(...), ...})

     Create a new graph with nodes ``a``, ``b``, ``c``, and so on.
     Initialize edges to ``graph[a:b] = ab_edge``, ``graph[b:a] = ba_edge``, and so on.

    .. note::
      If only a single argument is provided, graph and mapping initialization is preferred over iterable initialisation.
      To initialize a graph with a graph or mapping as the sole node, wrap it in an iterable, e.g. ``Graph([graph])``.

    All implementations of this ABC guarantee the following operators:

    .. describe:: bool(g)

       Whether there are any nodes in the graph ``g``.

    .. describe:: len(g)

      Return the number of nodes in the graph ``g``.

    .. describe:: g[a:b]

      Return the value of the edge between nodes ``a`` and ``b``. Raises :py:exc:`EdgeError` if
      no edge is defined for the nodes. Undirected graphs guarantee ``g[a:b] == g[b:a]``.

    .. describe:: g[a:b] = value

      Set the value of the edge between nodes ``a`` and ``b`` to ``value`` for graph ``g``.

    .. describe:: del g[a:b]

      Remove the edge and value between nodes ``a`` and ``b`` from ``g``.  Raises
      :exc:`EdgeError` if the edge is not in the graph.

    .. describe:: g[a]

      Return the edges between nodes ``a`` and any other node as an :py:class:`AdjacencyList`
      corresponding to ``{b: ab_edge, c: ac_edge, ...}``. Raises :py:exc:`NodeError` if
      ``a`` is not in ``g``.

    .. describe:: g[a] = True
                  g.add(a)

      Add the node ``a`` to graph ``g`` if it does not exist. Do not add, remove or modify existing edges.
      Graphs for which edges are computed, not set, may create them implicitly.

      .. versionchanged:: 0.3.0
        Added ``g[a] = True``, deprecated ``g[a] = a`` and ``g[a] = None``.

    .. describe:: g[a] = {}
                  g[a] = AdjacencyList()

      Add the node ``a`` to graph ``g`` if it does not exist. Remove any existing
      edges originating at ``a`` from graph ``g``.

    .. describe:: g[a] = {b: ab_edge, c: ac_edge, ...}
                  g[a] = AdjacencyList(b=ab_edge, c=c_edge)

      Add the node ``a`` to graph ``g`` if it does not exist. Set the value of the edge between
      nodes ``a`` and ``b`` to ``ab_edge``, between ``a`` and ``c`` to ``ac_edge``, and so on.
      Remove any other edge from ``a``. Raises :py:exc:`NodeError` if any of ``b``,
      ``c``, etc. are not in ``g``.

    .. describe:: del g[a]

      Remove the node ``a`` and all its edges from ``g``.  Raises
      :exc:`NodeError` if the node is not in the graph.

    .. describe:: a in g

      Return :py:const:`True` if ``g`` has a node ``a``, else :py:const:`False`.

    .. describe:: Edge[a:b] in g
                  Edge(a, b) in g

      Return :py:const:`True` if ``g`` has an edge from node ``a`` to ``b``, else :py:const:`False`.

    .. describe:: iter(g)

      Return an iterator over the nodes in ``g``.

    In addition, several methods are provided. While methods and operators for
    retrieving data must be implemented by all subclasses, methods for
    modifying data may not be applicable to certain graphs.
    """
    #: whether this graph is undirected, having only symmetric edges
    undirected = False

    def __init__(self, *source, **kwargs):
        """
        Initialize a new graph from another graph, iterable or mapping

        :param source: source for elements of the new graph
        :param kwargs: parameters for initialization
        """
        if not source:
            self.__init_empty__(**kwargs)
        elif len(source) == 1 and isinstance(source[0], Graph):
            self.__init_graph__(source[0], **kwargs)
        elif len(source) == 1 and isinstance(source[0], abc_collection.Mapping):
            self.__init_mapping__(source[0], **kwargs)
        elif len(source) == 1 and isinstance(source[0], abc_collection.Iterable):
            self.__init_iterable__(source[0], **kwargs)
        else:
            self.__init_iterable__(source, **kwargs)

    # initialize a new, empty graph
    def __init_empty__(self, **kwargs):
        self.__init_kwargs__(**kwargs)

    # initialize a new graph by copying nodes, edges and values from another graph
    def __init_graph__(self, graph, **kwargs):
        self.__init_kwargs__(**kwargs)

    # initialize a new graph by copying nodes from an iterable
    def __init_iterable__(self, iterable, **kwargs):
        self.__init_kwargs__(**kwargs)

    # initialize a new graph by copying nodes, edges and values from a nested mapping
    def __init_mapping__(self, mapping, **kwargs):
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

    # container interface
    def __len__(self):
        return sum(1 for _ in self)

    def __bool__(self):
        try:
            next(iter(self))
        except StopIteration:
            return False
        else:
            return True

    __nonzero__ = __bool__

    @abc.abstractmethod
    def __getitem__(self, item):
        # -- Get Edge
        # graph[node_a:node_b]
        # => graph.__getitem__(item=slice(a, b))
        # -- Get Node
        # graph[node_a]
        # => graph.__getitem__(item=node_a)
        raise NotImplementedError

    @abc.abstractmethod
    def __setitem__(self, item, value):
        # -- Set Edge
        # gr[node_a:node_b] = distance
        # => gr.__setitem__(item=slice(a, b), value=distance)
        # -- Set Node
        # gr[node_a] = {node_b: dist_b, node_c: dist_c}
        # => gr.__setitem__(item=node_a, value={node_b: dist_b, node_c: dist_c})
        raise NotImplementedError

    @abc.abstractmethod
    def __delitem__(self, item):
        # -- Delete Edge
        # del gr[node_a:node_b]
        # => gr.__delitem__(item=slice(a, b))
        # -- Delete Node
        # del gr[node_a]
        # => gr.__delitem__(item=node_a)
        raise NotImplementedError

    @abc.abstractmethod
    def __iter__(self):
        raise NotImplementedError

    def __contains__(self, item):
        if item.__class__ is slice:
            try:
                self[item]
            except EdgeError:
                return False
            else:
                return True
        else:
            return any(item == node for node in self)

    @abc.abstractmethod
    def clear(self):
        """Remove all elements from this graph"""
        raise NotImplementedError

    def copy(self):
        """Return a shallow copy of this graph"""
        return self.__class__(self)

    # graph views
    def nodes(self):
        """
        Return a new view of the graph's nodes

        :return: view of the graph's nodes
        :rtype: :py:class:`~.NodeView`
        """
        return NodeView(self)

    def edges(self):
        """
        Return a new view of the graph's edges

        :return: view of the graph's edges
        :rtype: :py:class:`~.EdgeView`
        """
        return EdgeView(self)

    def values(self):
        """
        Return a new view of the values of the graph's edges

        :return: view of the values of the graph's edges
        :rtype: :py:class:`~.ValueView`
        """
        return ValueView(self)

    def items(self):
        """
        Return a new view of the graph's edges and their values

        :return: view of the graph's edges and their values
        :rtype: :py:class:`~.ItemView`
        """
        return ItemView(self)

    # set-like graph methods
    def add(self, item):
        """
        Safely add a node or edge to the graph, without modifying existing edges

        If a :term:`node` is not part of the graph, it is added without any explicit edges.
        If a :term:`edge` is not part of the graph, its value is set to :py:const:`True`.

        .. note:: Graphs which compute edges may implicitly create new edges if ``node`` is new to the graph.
        """
        if item not in self:
            self[item] = True

    def discard(self, item):
        """
        Remove a node or edge from the graph if it is a member

        :param item: node or edge to discard from the graph
        """
        try:
            del self[item]
        except (NodeError, EdgeError):
            pass

    # dict-like graph methods
    def update(self, other):
        """
        Update the graph with the nodes, edges and values from ``other``,
        overwriting existing elements.

        :param other: graph or items from which to pull elements
        :type other: :py:class:`~.Graph` or :py:class:`~.ItemView`
        """
        if isinstance(other, (Graph, abc_collection.Mapping)):
            for node_from in other:
                self.add(node_from)
                node_adjacency = other[node_from]
                for node_to in node_adjacency:
                    self.add(node_to)
                    self[node_from:node_to] = node_adjacency[node_to]
        else:
            for node in other:
                self.add(node)

    def get(self, item, default=None):
        """
        Return the value for node or edge ``item`` if it is in the graph, else default. If
        ``default`` is not given, it defaults to :py:const:`None`, so that this method never
        raises a :py:exc:`NodeError` or :py:exc:`EdgeError`.

        :param item: node or edge to look up in the graph
        :param default: default to return if ``item`` is not in the graph
        """
        try:
            return self[item]
        except (NodeError, EdgeError):
            return default


class GraphView(abc_collection.Sized):
    """
    Dynamic view on the content of a :py:class:`~.Graph`

    View objects represent a portion of the content of a graph.
    A view allows to work with its scope without copying the viewed content.
    It is dynamic, meaning that any changes to the graph are reflected by the view.

    Each view works only on its respective portion of the graph.
    For example, ``edge in nodeview`` will always return :py:const:`False`.

    .. describe:: len(graphview)

      Return the number of nodes, node pairs or edges in the graph.

    .. describe:: x in graphview

      Return :py:const:`True` if x is a node, node pair or edge of the graph.

    .. describe:: iter(graphview)

      Return an iterator over the nodes, node pairs or edges in the graph.

    Each view strictly defines the use of nodes, edges or values.
    As such, edges are safely represented as a tuple of start and end node.
    """
    __slots__ = ('_graph',)

    @property
    def undirected(self):
        return self._graph.undirected

    def __init__(self, graph):
        self._graph = graph

    def __repr__(self):
        return '{0.__class__.__name__}({0._graph!r})'.format(self)


class NodeView(GraphView):
    """
    View on the nodes of a graph
    """
    __slots__ = ()

    def __iter__(self):
        return iter(self._graph)

    def __contains__(self, node):
        return node in self._graph

    def __len__(self):
        return len(self._graph)


class EdgeView(GraphView):
    """
    View on the edges in a graph
    """
    __slots__ = ()

    def __iter__(self):
        self_graph = self._graph
        for node_a, node_b in itertools.product(self_graph, repeat=2):
            edge_ab = edge.Edge(node_a, node_b)
            if edge_ab in self_graph:
                yield edge_ab

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
        return sum(1 for _ in self)


class ValueView(GraphView):
    """
    View on the values of edges in a graph
    """
    __slots__ = ()

    def __iter__(self):
        self_graph = self._graph
        for node_a, node_b in itertools.product(self_graph, repeat=2):
            try:
                yield self_graph[node_a:node_b]
            except (EdgeError, NodeError):
                continue

    def __contains__(self, value):
        self_graph = self._graph
        return any(self_graph[node_a:node_b] == value for node_a in self for node_b in self)

    def __len__(self):
        return sum(1 for _ in self)


class ItemView(GraphView):
    """
    View on the edges and values in a graph

    Represents edges and their value as a :py:class:`tuple` of ``(tail, head, value)``.
    For example, the edge ``graph[a:b] = c`` corresponds to the item ``(a, b, c)``.
    """
    __slots__ = ()

    def __iter__(self):
        self_graph = self._graph
        for node_a, node_b in itertools.product(self_graph, repeat=2):
            if edge.Edge(node_a, node_b) in self_graph:
                yield node_a, node_b, self_graph[node_a:node_b]

    def __contains__(self, edge_value):
        try:
            node_a, node_b, value = edge_value
            return self._graph[node_a:node_b] == value
        except (EdgeError, NodeError):
            return False

    def __len__(self):
        return sum(1 for _ in self)


class AdjacencyList(dict, abc_collection.MutableMapping):
    """
    Edge values of nodes to a node in a graph

    This represents edges in a ``graph`` originating from ``node`` as a mapping to their values.
    For example, the edge ``graph[a:b] = c`` corresponds to ``adjacency[b] = c`` for node ``a``.
    """
    __slots__ = ('__weakref__',)


@AdjacencyList.register
class AdjacencyView(GraphView):
    """
    View on the adjacency of edges for a node in a graph

    This represents edges in a ``graph`` originating from ``node`` as a mapping-like view.
    For example, the edge ``graph[a:b] = c`` corresponds to ``adjacency[b] = c`` for node ``a``.
    """
    __slots__ = ('_node',)

    def __init__(self, graph, node):
        super(AdjacencyView, self).__init__(graph)
        self._node = node

    def __getitem__(self, node):
        return self._graph[self._node:node]

    def __setitem__(self, node, value):
        self._graph[self._node:node] = value

    def __delitem__(self, node):
        del self._graph[self._node:node]

    def __iter__(self):
        self_graph, self_node = self._graph, self._node
        for node in self_graph:
            try:
                yield self_graph[self_node:node]
            except (EdgeError, NodeError):
                continue

    def __len__(self):
        return sum(1 for _ in self)

    def __contains__(self, node):
        return edge.Edge(self._node, node) in self._graph
