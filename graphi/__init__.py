from .abc import Graph as _GraphABC
from .types.adjacency_graph import AdjacencyGraph as _AdjacencyGraph

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
graph = _AdjacencyGraph

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

__all__ = ['graph', 'GraphABC']
