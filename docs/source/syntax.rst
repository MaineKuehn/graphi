++++++++++++
Graph Syntax
++++++++++++

Graphs use both key and slice notation to refer to :term:`nodes <node>` and :term:`edges <edge>`, respectively.
This works for both assignment and lookup of the respective value.

Nodes
-----

A :term:`node` is written directly.
Its value is the adjacency associated with the node in the graph,
i.e. a mapping to all :term:`neighbours <neighbour>` and the respective :term:`edge value`.

.. math::

    \mathtt{
        \underbrace{\vphantom{\bigl[}\mathtt{flighttime}}_\mathtt{graph}
            [\underbrace{\vphantom{\bigl[}\mathtt{Berlin}}_\mathtt{node}]
            =
            \overbrace{
              \{
                \underbrace{\vphantom{\bigl[}\mathtt{London}}_\mathtt{node}
                :
                \underbrace{\vphantom{\bigl[}\mathtt{3900}}_\mathtt{value}
                , ...
              \}
            }^\mathtt{adjacency}
    }

Edges
-----

An :term:`edge` is written using :term:`slice` notation.
Its value is the :term:`edge value` associated with the edge in the graph.

.. math::

    \mathtt{
        \underbrace{\vphantom{\bigl[}\mathtt{flighttime}}_\mathtt{graph}
            [\overbrace{
                \underbrace{\vphantom{\bigl[}\mathtt{Berlin}}_\mathtt{node}
                :
                \underbrace{\vphantom{\bigl[}\mathtt{London}}_\mathtt{node}
            }^{edge}] = \underbrace{\vphantom{\bigl[}\mathtt{3900}}_\mathtt{value}
    }
