++++++++++++++++
graphi Changelog
++++++++++++++++

prerelease 2017-??-??
---------------------

    **Notes**
        Added operator interface and implementations

        Added graph input/output

    **Major Changes**
        Added ``graph[item] = True``, which is equal to ``graph.add(item)``.
        Deprecates both ``graph[node] = node`` and ``graph[node] = None``.

    **New Features**
        Operator interface allowing graphs to provide optimized implementations

        Added operators:

            - ``neighbours(graph, node, ..)``

        Added input/output:

            - csv

0.2.0 2017-07-31
----------------

    **Notes**
        Definition of primary interface, algorithms (``Graph.neighbours``) will be revised

    **New Features**
        Added AdjacencyGraph

    **Major Changes**
        Defined graph container interface

    **Minor Changes**
        Added documentation
