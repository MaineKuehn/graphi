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

    outdegree
        The number of outgoing edges of a node.
        If a node has a :term:`loop`, it also counts as an outgoing edge.

    degree
        The number of ingoing and outgoing edges of a node.
        If a node has a :term:`loop`, it counts as both an ingoing and outgoing edge.

        The :term:`degree` of a node is the sum of its :term:`indegree` and :term:`outdegree`.
