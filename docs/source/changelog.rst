++++++++++++++++
graphi Changelog
++++++++++++++++

prerelease 201?-??-??
---------------------

    **Overview**
        Added operator interface and implementations

        Added graph input/output

        Added Cython graph implementation

    **Major Changes**
        Added ``graph[item] = True``, which is equal to ``graph.add(item)``.
        Deprecates both ``graph[node] = node`` and ``graph[node] = None``.

        The class ``graphi.graph`` always uses the best implementation available

    **New Features**
        Operator interface allowing graphs types to use optimized implementations

        Added operators:

            - ``neighbours(graph, node, ..)``

            - ``density(graph)``

        Added input formats:

            - csv

            - GraphML

    **Minor Changes**

        Graphs explicitly define ``bool(graph)``.
        This was previously implicitly available as ``bool`` falls back to ``__len__``.

0.2.0 2018-07-31
----------------

    **Notes**
        Definition of primary interface, algorithms (``Graph.neighbours``) will be revised

    **New Features**
        Added AdjacencyGraph

    **Major Changes**
        Defined graph container interface

    **Minor Changes**
        Added documentation
