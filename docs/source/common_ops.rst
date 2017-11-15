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

.. describe:: graph.add(a)

    Safely add a :term:`node` ``a`` to ``graph``.

.. describe:: del graph[a]

    Remove a :term:`node` ``a`` from ``graph``.

.. describe:: a in graph

    Whether there is a :term:`node` ``a`` in ``graph``.

.. describe:: list(graph)
              iter(graph)
              for a in graph:

    List/iterate/loop all :term:`nodes <node>` ``a`` in ``graph`` .

.. describe:: len(graph)

    The number of :term:`nodes <node>` in the graph.

Edges and values of a graph
---------------------------

.. describe:: graph[a:b] = w

    Add an :term:`edge` from :term:`node` ``a`` to :term:`node` ``b`` with :term:`value <edge value>` ``w``.

.. describe:: Edge[a:b] in graph

    Whether there is an :term:`edge` from :term:`node` ``a`` to :term:`node` ``b`` in ``graph``.

.. describe:: Loop[a] in graph
              Edge[a:a] in graph

    Whether there is a :term:`loop` from :term:`node` ``a`` to itself in ``graph``.

.. describe:: list(graph[a])
              iter(graph[a])
              for b in graph[a]:

    List/iterate/loop all :term:`nodes <node>` ``b`` for which there is an
    edge from :term:`node` ``a`` to :term:`node` ``b``.

.. describe:: len(graph[node])

    The number of outgoing :term:`edges <edge>` of a :term:`node`, i.e. its :term:`outdegree`.
