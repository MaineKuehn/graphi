"""
Utilities for loading and storing Graphs
"""
import csv
import ast
import itertools

try:
    from collections import abc as abc_collection
except ImportError:
    import collections as abc_collection

from ..types import adjacency_graph


class DistanceMatrixLiteral(csv.Dialect):
    """
    CSV dialect for a Graph Matrix Literal, suitable for numeric data and string literals

    ```
     a   b   c
     0   2 1.3
     2   0  .5
    16  .5   1
    ```
    """
    #: no explicit delimeters required
    delimiter = ' '
    #: string literals can be written as "foo"
    quotechar = "'"
    doublequote = False
    #: use regular escaping
    escapechar = "\\"
    #: allow for alignment with arbitrary whitespace
    skipinitialspace = True
    quoting = csv.QUOTE_MINIMAL
    lineterminator = '\n'


def stripped_literal(literal):
    """
    evaluate literals, ignoring leading/trailing whitespace

    This function is capable of handling all literals supported by
    :py:func:`ast.literal_eval`, even if they are surrounded by whitespace.
    """
    return ast.literal_eval(literal.strip())


def graph_reader(
        iterable,
        nodes_header=True,
        literal_type=stripped_literal,
        valid_edge=bool,
        undirected=False,
        *args,
        **kwargs
):
    """
    Utility for reading a graph from files or iterables

    :param iterable: an iterable yielding lines of CSV
    :param nodes_header: whether and how to interpret a header specifying nodes
    :param literal_type: type callable to evaluate literals
    :param valid_edge: callable to test whether an edge should be inserted
    :param undirected: whether to mirror the underlying matrix

    The `iterable` argument can be any object that returns a line of
    input for each iteration step, such as a file object or a list.

    Nodes are created depending on the value of `nodes_header`:

    :py:const:`False`
      Nodes are numbered ``1`` to ``len(iterable[0])``. Elements in the first
      line of ``iterable`` are *not* consumed by this.

    iterable
      Nodes are read from `node_header`.

    :py:const:`True`
      Nodes are taken as the elements of the first line of ``iterable``. The
      first line is consumed by this, and not considered as containing graph
      edges. Nodes are read plainly of type :py:class:``str``, not using ``literal_type``.

    callable
      Like :py:const:`True`, but nodes are not taken as plain :py:func:`str`
      but individually interpreted via ``node_header(element)``.

    The CSV is interpreted as a matrix, where the row marks the origin of an
    edge and the column marks the destination. Thus, loops are specified on the diagonal,
    while an asymmetric matrix creates different edge values for opposite directions.
    For an ``undirected`` graph, the matrix is automatically treated as symmetric.
    Trailing empty lines may be removed.

    In the following example, the edges ``a:b`` and ``a:c`` are symmetric and there
    are no edges or self-loops ``a:a`` or ``b:b``. In contrast, ``b:c`` is 3 whereas
    ``c:b`` is ``4``, and there is a self-loop ``c:c``. The node ``d`` only has an
    ingoing edge ``b:d``, but no outgoing edges.
    ```
    a  b  c  d
    0  2  1  0
    2  0  3  2
    1  4  1  0
    ```

    If ``undirected`` evaluates to :py:const:`True`, the upper right corner is mirrored to
    the lower left. Note that the diagonal *must* be provided. The following
    matrices give the same output if ``symmetric`` is :py:const:`True`:
    ```
    a  b  c    a  b  c    a  b  c
    0  2  1    0  2  1    0  2  1
    2  0  3       0  3    5  0  3
    1  4  1          1    7     1
    ```

    Evaluation and

    .. function:: literal_type(literal) -> object

        Fields read from the csv are passed to `literal_type` directly as the
        sole argument. The return value is considered as final, and inserted
        into the graph without further conversions.

    .. function:: valid_edge(object) -> bool

        Similarly, `valid_edge` is called on the result of `literal_type`.
        The default is :py:func:`bool`, which should work for most data types.

    The default for `literal_type` is capable of handling literals,
    e.g. :py:class:`int`, :py:class:`float` and :py:class:`str`. In combination with
    `valid_edge`, any literal of non-True values signifies a missing edge:
    `None`, `False`, `0` etc.

    :see: The `*args` and `**kwargs` are passed on directly to
          :py:class:`csv.reader` for extracting lines.
    """
    reader = csv.reader(iterable, *args, **kwargs)
    first_line = next(reader)
    if nodes_header is False:
        first_line = list(first_line)
        nodes = range(len(first_line))
    elif nodes_header is True:
        nodes = list(first_line)
        first_line = None
    elif isinstance(nodes_header, abc_collection.Iterable):
        nodes = list(nodes_header)
    elif callable(nodes_header):
        nodes = [nodes_header(element) for element in first_line]
        first_line = None
    else:
        raise TypeError("parameter 'nodes_header' must be True, False, an iterable or a callable")
    # fill graph with nodes
    graph = adjacency_graph.AdjacencyGraph(nodes, undirected=undirected)
    # still need to consume the first line as content if not unset
    iter_rows = reader if first_line is None else itertools.chain([first_line], reader)
    for row_idx, row in enumerate(iter_rows):
        node_from = nodes[row_idx]
        for idx, literal in enumerate(row if not undirected else row[-len(nodes) + row_idx:]):
            node_to = nodes[idx] if not undirected else nodes[row_idx + idx]
            edge = literal_type(literal.strip())
            if not valid_edge(edge):
                continue
            graph[node_from:node_to] = edge
            if undirected and node_to != node_from:
                graph[node_to:node_from] = edge
    return graph