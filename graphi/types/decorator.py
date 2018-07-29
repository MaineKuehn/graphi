from .. import abc


def boundable(graph_class):
    assert issubclass(graph_class, abc.Graph), 'only subclasses of Graph can be bounded'
    __new__ = graph_class.__new__

    @staticmethod
    def __new_graph__(cls, *args, **kwargs):
        value_bound = kwargs.pop('value_bound', None)
        super_new = __new__
        if super_new is object.__new__:
            self = super_new(cls)
        else:
            self = super_new(cls, *args, **kwargs)
        if value_bound is not None:  # replicates type.__call__
            if isinstance(self, cls):
                self.__init__(*args, **kwargs)
            return Bounded(self, value_bound=value_bound)
        else:
            return self

    graph_class.__new__ = __new_graph__
    return graph_class


def undirectable(graph_class):
    """
    Make an implementation of :py:class:`~.abc.Graph` undirectable by passing ``undirected=True`` to it

    .. code:: python

        @undirectable
        class SomeGraph(abc.Graph):
            ...

        directed_graph = SomeGraph()
        undirected_graph = SomeGraph(undirected=True)

    This provides an implementation agnostic interface to ensure all edges are undirected.
    For any :term:`nodes <node>` ``a`` and ``b``, ``graph[a:b] == graph[b:a]`` always holds and
    ``graph.edges()`` produces only one of ``a:b`` or ``b:a``.
    """
    assert issubclass(graph_class, abc.Graph), 'only subclasses of Graph can be undirected'
    __new__ = graph_class.__new__

    @staticmethod
    def __new_graph__(cls, *args, **kwargs):
        undirected = kwargs.pop('undirected', False)
        super_new = __new__
        if super_new is object.__new__:
            self = super_new(cls)
        else:
            self = super_new(cls, *args, **kwargs)
        if undirected:  # replicates type.__call__
            if isinstance(self, cls):
                self.__init__(*args, **kwargs)
            return Undirected(self)
        else:
            return self

    graph_class.__new__ = __new_graph__
    return graph_class


from .undirected import Undirected
from .bounded import Bounded
