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

.. describe:: len(graph[node])

    The number of outgoing edges of a node, i.e. its :term:`outdegree`.

.. describe:: Edge[node:node] in graph

    Whether there is a :term:`loop` for ``node`` in ``graph``.
