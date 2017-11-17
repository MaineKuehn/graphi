++++++++
Glossary
++++++++

.. glossary::

    loop
        An edge from a node to itself.
        Counts as both an ingoing *and* outgoing edge for :term:`outdegree`, :term:`indegree` and :term:`degree`.

    indegree
        The number of ingoing edges of a node.
        If a node has a :term:`loop`, it also counts as an ingoing edge.

        The number of nodes to which a node is a :term:`neighbour`.

    outdegree
        The number of outgoing edges of a node.
        If a node has a :term:`loop`, it also counts as an outgoing edge.

        The number of :term:`neighbours <neighbour>` of a node.

    degree
        The number of ingoing and outgoing edges of a node.
        If a node has a :term:`loop`, it counts as both an ingoing and outgoing edge.

        The :term:`degree` of a node is the sum of its :term:`indegree` and :term:`outdegree`.

    graph
        A collection of :term:`nodes <node>`, :term:`edges <edge>` between them
        and possibly :term:`values <edge value>` associated with any :term:`edges <edge>`.

    node
        A regular object in a :term:`graph`.

    edge
    arrow
        A connection between two :term:`nodes <node>` in a :term:`graph`.

    edge value
    weight
        The value associated with an :term:`edge` in a :term:`graph`.

    neighbour
        A :term:`node` with an :term:`edge` from a specific node.
        Given an edge ``a:b``, ``b`` is a :term:`neighbour` of ``a``.

        The number of neighbours is the :term:`outdegree`.
