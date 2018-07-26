from __future__ import absolute_import

import six


class EdgeMeta(type):
    """
    Metaclass for :py:class:`Edge` to support ``Edge[a:b]``
    """
    def __getitem__(cls, item):
        if not isinstance(item, slice):
            raise TypeError('Edge must be slice-like')
        return cls(item.start, item.stop, item.step)


@six.add_metaclass(EdgeMeta)
class Edge(object):
    """
    An edge in a graph as a pair of nodes

    :param start: the start or tail of an edge
    :param stop: the stop or head of an edge
    :param step: currently unused

    This is a verbose interface for creating edges between nodes for use in a graph.
    It allows using slice notation independent of a graph:

    .. code:: python

        >>> atb = Edge[a:b]
        >>> a2b = Edge(a, b)
        >>> graph[a2b] = 1337
        >>> graph[a:b] == graph[atb] == graph[a2b] == graph[Edge[a:b]] == graph[Edge(a, b)]
        True

    A :py:class:`~.Edge` can also be used for explicit containment tests:

    .. code:: python

        >>> Edge[a:b] in graph
        True

    In addition to their slice-like nature, :py:class:`Edge` is iterable and indexable.
    This allows for easy unpacking:

    .. code:: python

        >>> edge = Edge[a:b]
        >>> tail, head = edge

    .. note:: This class creates a representation of an edge as a connection between nodes.
              Edge *values* can be arbitrary objects.

    .. warning:: Even though :py:class:`~.Edge` behaves like a :py:class:`slice` in graphs,
                 builtin containers such as :py:class:`list` cannot make use of an :py:class:`~.Edge`.
    """
    __slots__ = ('start', 'stop')

    def __init__(self, start, stop, step=None):
        self.start = start
        self.stop = stop
        if step is not None:
            raise TypeError('%s does not support a third argument' % type(self).__name__)

    @property
    def __class__(self):
        # pretend to be a slice
        # MF@20170718
        # As of Py3.6, it is not possible nor meaningful to create subclasses of ``slice``.
        # However, faking __class__ is sufficient for testing ``foo.__class__ is slice``
        # and ``isinstance(foo, slice)``. Since these are the fastest and broadest python tests,
        # all of graphi should use one of them.
        # Note that a C-level test using ``PySlice_Check`` *cannot* be tricked, and will identify
        # this class as not-slice. This means it cannot be used for builtin types.
        return slice

    def __getitem__(self, index):
        return [self.start, self.stop][index]

    def __iter__(self):
        yield self.start
        yield self.stop

    def __str__(self):
        return '[%s:%s]' % (self.start, self.stop)

    def __eq__(self, other):
        if not isinstance(self, type(other)):
            return NotImplemented
        return self.start == other.start and self.stop == other.stop

    def __repr__(self):
        return '%s[%r:%r]' % (type(self).__name__, self.start, self.stop)


class Loop(Edge):
    """
    An edge in a graph from a node to itself

    :param start: the start or tail of a loop
    :param stop: optional stop or head of a loop, same as start
    :param step: currently unused

    :raises ValueError: if ``stop`` is given but not equal to ``start``
    """
    def __init__(self, start, stop=None, step=None):
        stop = start if stop is None else stop
        if start != stop:
            raise ValueError('%s start and stop node must be equal' % self.__class__.__name__)
        super(Loop, self).__init__(start, stop, step)
