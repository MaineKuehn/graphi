import functools


DEFAULT_OPERATOR_PREFIX = __name__.split('.')[0]


def graph_operator(prefix=DEFAULT_OPERATOR_PREFIX):
    """
    Implement a callable as a graph operator

    :param prefix: identifier to prepend to special method names

    Adds the operator lookup and fallback procedure to allow
    :py:class:`~graphi.abc.Graph` subclasses to implement optimized algorithms.
    For example, a graph storing edges in a sorted data structure may prematurely
    end a search for neighbours given a maximum distance.

    A graph can influence the evaluation of a graph operator by providing an attribute
    named ``__<prefix>_<operator name>__``, e.g. ``__graphi_neighbours__`` for an operator ``neighbours``.
    If this is the case, the attribute is called with the provided arguments as a replacement
    for the operator implementation.

    .. py:function:: operator(graph, *args, **kwargs)

        The generic implementation of a graph operator.

    .. py:method:: graph.__graphi_operator__(*args, **kwargs)

        The optimized implementation of a graph operator.

    There are three special conditions to this procedure:

    attribute is :py:const:`None`
        The graph does not support the operation.

        Attempting the operation on the graph raises :py:exc:`TypeError`.

    attribute is :py:const:`NotImplemented`
        The graph does not overwrite the operation.
        The operator implementation is always used.

    calling the attribute returns :py:const:`NotImplemented`
        The graph does not overwrite the operation for the specific parameters.
        The operator implementation is used.

    The name of an operator is taken from ``operator.__name__`` or ``operator.__class__.__name__``.
    """
    def wrap_operator(operator):
        try:
            operator_name = operator.__name__
        except AttributeError:
            operator_name = operator.__class__.__name__
        override_name = '__%s_%s__' % (prefix, operator_name)

        @functools.wraps(operator)
        def wrapped_operator(graph, *args, **kwargs):
            graph_op = getattr(graph, override_name, NotImplemented)
            if graph_op is None:
                raise TypeError(
                    'object of type %r does not support %r graph operator' % type(graph).__name__, operator.__name__
                )
            if graph_op is not NotImplemented:
                return_value = graph_op(*args, **kwargs)
            else:
                return_value = NotImplemented
            if return_value is not NotImplemented:
                return return_value
            return operator(graph, *args, **kwargs)
        wrapped_operator.override_name = override_name
        return wrapped_operator
    if not isinstance(prefix, str):
        _operator = prefix
        prefix = DEFAULT_OPERATOR_PREFIX
        return wrap_operator(_operator)
    return wrap_operator
