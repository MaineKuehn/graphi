from .abc import Graph as _GraphABC
from .edge import Edge as _Edge
try:
    from .types.cython_graph import CythonGraph as _DefaultGraph
except ImportError:
    from .types.adjacency_graph import AdjacencyGraph as _DefaultGraph


#: Default graph type implementation
#:
#: An implementation of the :py:class:`~graphi.abc.Graph` interface,
#: suitable for most purposes.
#: Support of all graph interfaces for both reading and writing is
#: provided.
#: The implementation is adequate for most use-cases, and provides
#: a balance of complexity, performance and storage.
#:
#: :see: The corresponding class
#:       :py:class:`~graphi.types.adjacency_graph.AdjacencyGraph`
#:       for details.
graph = _DefaultGraph

#: Graph :term:`abstract base class` for type checks and virtual subclasses
#:
#: The ABC is primarily needed for two cases:
#:
#: * Type checking to find graph classes via :py:func:`isinstance`, as in
#:   ``isinstance(candidate, GraphABC)``.
#:
#: * Actual or virtual subclasses acting as implementations of the :py:mod:`graphi`
#:   interface for type checks.
#:
#: :see: The corresponding class
#:       :py:class:`~graphi.abc.Graph`
#:       for details.
GraphABC = _GraphABC

#: Rich representation of :term:`edges <edge>` as ``[start:end]`` pairs
#:
#: Convenience interface to define and work with :term:`edges <edge>`
#: outside of graphs. This primarily allows to store edges and to test
#: whether edges are in a graph.
#:
#: :note: Graphs only guarantee to store ``start`` and ``end``.
#:        Any information stored on an ``Edge`` is not preserved
#:        by the :term:`graph`.
Edge = _Edge

__all__ = ['graph', 'GraphABC', 'Edge']
