+++++++++++++++++++++
Quick Usage Reference
+++++++++++++++++++++

``GraphI`` is primarily meant for working directly on graph data.
The primitives you need to familiarise yourself with are

1. graphs, which are extended containers,

2. nodes, which are arbitrary objects in a graph,

3. edges, which are connections between objects in a graph, and

4. edge values, which are values assigned to connections in a graph.

.. graphviz::

    digraph graphname {
        graph [rankdir=LR, label="graph(a, b, c)"]
        subgraph cluster_c {
            label=""
            a -> c [label="[b:c]=2"]
            b -> c [label="[a:c]=3"]
            a -> b [label="[c:b]=5"]
        }
    }

This documentation page gives an overview of the most important aspects.
The complete interface of ``GraphI`` is defined and documented by :py:class:`~graphi.abc.Graph`.

Creating Graphs and adding Nodes
================================

You can create graphs empty, via cloning, from nodes or with nodes, edges and values.
For many use-cases, it is simplest to start with a set of nodes:

.. code::

    from graphi import graph

    planets = graph("Earth", "Jupiter", "Mars", "Pluto")

Once you have a graph, it works similar to a :py:class:`set` for nodes.
You can simply :py:meth:`~graphi.abc.Graph.add` and :py:meth:`~graphi.abc.Graph.discard` nodes:

.. code::

    planets.add("Venus")
    planets.add("Mercury")
    planets.discard("Pluto")

Working with Edges and Values
=============================

To really make use of a graph, you will want to add edges and give them values.
Simply pick a connection *from* a node *to* a node and assign it a value:

.. code::

    # store the average distance between planets
    planets["Earth":"Venus"] = 41400000

An edge is always of the form ``start:end``, but values can be of arbitrary type.
For example, you can easily add multiple values for a single edge using containers:

.. code::

    # add multiple values as an implicit tuple
    planets["Earth":"Venus"] = 41400000, 258000000
    # add multiple values as an explicit, mutable list
    planets["Earth":"Mars"] = [78000000, 378000000]

The ``:``-syntax of edges is not just pretty - it ensures that you never, ever accidentally mix up nodes and edges.
This allows you to safely use the same ``graph[item]`` interface for nodes and edges.

If you need to define an edge outside of graph accesses, explicitly use :py:class:`~graphi.edge.Edge`:

.. code::

    from graphi import Edge

    if Edge["Venus":"Earth"] in planets:
        print("Wait, isn't there a pattern for this?")

Graphs as Python Containers
===========================

``GraphI`` is all about letting you handle graphs with well-known interfaces.
A graph is a container indexed by either nodes or edges:

.. code::

    print(planets["Venus":"Earth"])
    del planets["Jupiter"]

Even though it contains nodes, edges and values, it presents its nodes first - similar to keys in a :py:class:`dict`.
However, you can efficiently access its various elements via views:

.. code::

    print("My father only told me about %d of our planets." % len(planets))
    print("But I looked up %d distances between planets:" % len(planets.edges())
    for planet_a, planet_b, distances in planets.items():
        print("  %s to %s: %s" % (planet_a, planet_b, '-'.join(distances)))
