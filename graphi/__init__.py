"""
++++++++++++++++++++++++++
GraphI - Graphs for Humans
++++++++++++++++++++++++++

Documentation is available in docstrings of modules, classes and functions.
In an interactive session, use ``help``, or ipython's ``?`` and ``??``.
For example, use ``help(graphi.GraphABC)`` to view the graph interface.

For further help, tutorials and examples visit
http://graphi.readthedocs.io
to view the full documentation.

Using Graphs
++++++++++++

You should start by using the type ``graphi.graph`` - the most well-rounded
graph implementation on your system.  Like all ``graphi`` types, it uses an
interface similar to the Python builtin types:

.. code:: python

    from graphi import graph

    # create a graph with initial nodes
    airports = graph("New York", "Rio", "Tokyo")

    # add connections between nodes
    airports["New York":"Rio"] = timedelta(hours=9, minutes=50)
    airports["New York":"Tokyo"] = timedelta(hours=13, minutes=55)
"""
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
