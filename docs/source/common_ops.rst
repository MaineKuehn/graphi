+++++++++++++++++++++++
Common Graph Operations
+++++++++++++++++++++++

Many common graph operations map to simple operators in :py:mod:`graphi`.
Unless parameters are needed, builtin operations usually suffice.
For example, the outdegree of a node is simply its number of outgoing edges, i.e.

.. code::

    out_degree = len(graph[node])

in a directed graph.
Since :py:mod:`graphi` makes heavy use of data views (instead of copies), this has optimal performance.

Pythonic Graph Operations
+++++++++++++++++++++++++

Nodes of a graph
----------------

Graphs behave like a :py:class:`set` with regard to :term:`nodes <node>`.
Note that removing a :term:`node` also invalidates all its :term:`edges <edge>` and their :term:`values <edge value>`.

.. describe:: graph[a] = True
              graph.add(a)
              graph.discard(a)

    Safely add or remove a :term:`node` ``a`` from ``graph``.

.. describe:: del graph[a]

    Remove a :term:`node` ``a`` from ``graph``.

.. describe:: a in graph

    Whether there is a :term:`node` ``a`` in ``graph``.

.. describe:: list(graph)
              iter(graph)
              for a in graph:

    List/iterate/traverse all :term:`nodes <node>` in ``graph`` .

.. describe:: len(graph)

    The number of :term:`nodes <node>` in the graph.

Edges and values of a graph
---------------------------

Graphs special-case :term:`edges <edge>`: an :term:`edge` is a secondary key,
being the value to :term:`nodes <node>` and the key to :term:`edge values <edge value>`.

.. describe:: Edge[a:b] in graph

    Whether there is an :term:`edge` from :term:`node` ``a`` to :term:`node` ``b`` in ``graph``.

.. describe:: Loop[a] in graph
              Edge[a:a] in graph

    Whether there is a :term:`loop` from :term:`node` ``a`` to itself in ``graph``.

.. describe:: list(graph[a])
              iter(graph[a])
              for b in graph[a]:

    List/iterate/loop all :term:`nodes <node>` for which there is an
    edge from :term:`node` ``a``, i.e. its :term:`neighbours <neighbour>`.

.. describe:: len(graph[a])

    The number of outgoing :term:`edges <edge>` of :term:`node` ``a``, i.e. its :term:`outdegree`.

Edge values of a graph
----------------------

Graphs behave similar to a :py:class:`dict`, tying :term:`values <edge value>` to :term:`edges <edge>`.
Note that removing a :term:`node` also invalidates all its :term:`edges <edge>` and their :term:`values <edge value>`.

.. describe:: graph[a:b] = w
              graph[Edge[a:b]] = w

    Add an :term:`edge` from :term:`node` ``a`` to :term:`node` ``b`` with :term:`value <edge value>` ``w``.

Pythonic Graph Types
++++++++++++++++++++

By default, every graph is a weighted, directed graph
- :term:`edges <edge>` are oriented from start to end :term:`node` and have one :term:`edge value`.
However, other graph types can be created with standard language features.

.. describe:: graph[a:b] = True

    Add an :term:`edge` from :term:`node` ``a`` to :term:`node` ``b`` with
    the primitive :term:`value <edge value>` :py:const:`True`.

    This creates an unweighted graph edge.

.. describe:: graph[a:b] = [w1, w2, w3, ...]
              graph[a:b] = w1, w2, w3, ...

    Add an :term:`edge` from :term:`node` ``a`` to :term:`node` ``b`` with
    multiple :term:`values <edge value>` ``w1, w2, w3, ...``.

    This creates a multigraph edge.

.. describe:: graph[a:b] = graph[b:a] = w

    Add :term:`edge`\ s from :term:`node` ``a`` to :term:`node` ``b`` and
    from :term:`node` ``b`` to :term:`node` ``a``
    with
    the identical :term:`value <edge value>` ``w``.

    This creates an undirected graph edge.

Abstract Graph operations
+++++++++++++++++++++++++

The common abstract `Graph Operations`_ interface can be mapped to :py:mod:`graphi` almost directly.
Most operations map to container accesses via ``[item]``, and an :term:`edge` is represented as ``x:y``.

+--------------------------+--------------------------------+-----------------------------------------------------------------------------------+
| Graphi                   | Abstract Graph Operation       |                                                                                   |
+==========================+================================+===================================================================================+
| ``G.add(x)``             | ``add_vertex(G, x)``           | adds the node ``x``                                                               |
+--------------------------+--------------------------------+-----------------------------------------------------------------------------------+
| ``G.discard(x)``         | ``remove_vertex(G, x)``        | removes the node ``x``                                                            |
+--------------------------+--------------------------------+-----------------------------------------------------------------------------------+
| ``del G[x]``             | N/A                            | ..., but raises ``NodeError`` if there is no node ``x``                           |
+--------------------------+--------------------------------+-----------------------------------------------------------------------------------+
| ``G.add(Edge[x:y])``     | ``add_edge(G, x, y)``          | adds an edge from node ``x`` to node ``y``                                        |
+--------------------------+--------------------------------+-----------------------------------------------------------------------------------+
| ``G.discard(Edge[x:y])`` | ``remove_edge(G, x, y)``       | removes the edge from node ``x`` to node ``y``                                    |
+--------------------------+--------------------------------+-----------------------------------------------------------------------------------+
| ``del G[x:y]``           | N/A                            | ..., but raises ``EdgeError`` if there is no edge from node ``x`` to node ``y``   |
+--------------------------+--------------------------------+-----------------------------------------------------------------------------------+
| ``Edge[x:y] in G``       | ``adjacent(G, x, y)``          | tests whether there is an edge from node ``x`` to node ``y``                      |
+--------------------------+--------------------------------+-----------------------------------------------------------------------------------+
| ``G[x:y]``               | N/A                            | raises ``EdgeError`` if there is no edge from node ``x`` to node ``y``            |
+--------------------------+--------------------------------+-----------------------------------------------------------------------------------+
| ``list(G[x])``           | ``neighbors(G, x)``            | lists all nodes ``y`` with an edge from node ``x`` to node ``y``                  |
+--------------------------+--------------------------------+-----------------------------------------------------------------------------------+
| N/A                      | ``get_vertex_value(G, x)``     | returns the value associated with node ``x``                                      |
+--------------------------+--------------------------------+-----------------------------------------------------------------------------------+
| N/A                      | ``set_vertex_value(G, x, v)``  | sets the value associated with node ``x`` to ``v``                                |
+--------------------------+--------------------------------+-----------------------------------------------------------------------------------+
| ``G[x:y]``               | ``get_edge_value(G, x, y)``    | returns the value associated with the edge ``x:y``                                |
+--------------------------+--------------------------------+-----------------------------------------------------------------------------------+
| ``G[x:y] = w``           | ``set_edge_value(G, x, y, v)`` | sets the value associated with the edge ``x:y`` to ``v``                          |
+--------------------------+--------------------------------+-----------------------------------------------------------------------------------+

Note that there is no concept for associating a value to a :term:`node` in a graph -
for a node ``x``, ``G[x]`` is the adjacency list.
Instead, use a separate :py:class:`dict` to assign external values to nodes,
or set values directly on nodes.

.. _`Graph Operations`: https://en.wikipedia.org/wiki/Graph_(abstract_data_type)
