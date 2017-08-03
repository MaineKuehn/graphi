+++++++++++++++++++++++
Common Graph Operations
+++++++++++++++++++++++

Many common graph operations map to simple operators in :py:mod:`graphi`.
Unless parameters are needed, builtin operations usually suffice.
For example, the outdegree of a node is simply

.. code::

    len(graph[node])

in a directed graph.
Since :py:mod:`graphi` makes heavy use of data views (instead of copies), this has optimal performance.
