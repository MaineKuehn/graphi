from .. import abc

from .decorator import undirectable


@undirectable
class DistanceGraph(abc.Graph):
    r"""
    Graph of nodes connected by a distance function

    :param nodes: all nodes contained in the graph
    :param distance: a function `dist(a, b)->object` that computes the distance between any two nodes
    :param undirected: whether distance can be treated as undirected, i.e. `dist(a, b) == dist(b, a)`

    :warning: For N nodes, all NxN edges are exposed. This may lead to
              O(N\ :sup:2\ ) runtime complexity.
    """
    def __init__(self, *source, **kwargs):
        distance = kwargs.pop("distance", None)
        maximum_distance = kwargs.pop("maximum_distance", float("Inf"))
        assert distance
        self.undirected = kwargs.pop("undirected", True)
        self._nodes = set()
        super(DistanceGraph, self).__init__(*source, **kwargs)
        self.distance = distance
        self.maximum_distance = maximum_distance

    # initialize a new graph by copying nodes from an iterable
    def __init_iterable__(self, iterable, **kwargs):
        for node in iterable:
            self._nodes.add(node)

    def __getitem__(self, item):
        # a:b -> slice -> edge
        if isinstance(item, slice):
            assert item.step is None, '%s does not support stride argument for edges' % self.__class__.__name__
            node_from, node_to = item.start, item.stop
            if node_from not in self._nodes:
                raise abc.EdgeError  # first edge node
            elif node_to not in self._nodes:
                raise abc.EdgeError  # second edge node
            # Since we don't know the type of nodes, we cannot test
            # node_to > node_from to detect swapped pairs. Since we
            # *do* store nodes in a `set`, they must support hash.
            if self.undirected and hash(node_to) > hash(node_from):
                node_to, node_from = node_from, node_to
            return self.distance(node_from, node_to)
        else:
            if item not in self:
                raise abc.NodeError
            return {candidate: self[item:candidate] for candidate in self if candidate != item}

    def __setitem__(self, item, value):
        if value or isinstance(item, slice):
            raise TypeError('%s does not support edge assignment' % self.__class__.__name__)
        else:
            self._nodes.add(item)

    def __delitem__(self, item):
        # a:b -> slice -> edge
        if isinstance(item, slice):
            raise TypeError('%s does not support edge deletion' % self.__class__.__name__)
        else:
            try:
                self._nodes.remove(item)
            except KeyError:
                raise abc.NodeError

    def __iter__(self):
        return iter(self._nodes)

    def __add__(self, other):
        if isinstance(self, other.__class__) and self.distance == other.distance:
            return self.__class__(
                self._nodes.union(other),
                distance=self.distance,
                undirected=self.undirected and other.undirected)
        return NotImplemented

    def clear(self):
        self._nodes = type(self._nodes)()

    def update(self, other):
        if isinstance(self, other.__class__) and self.distance == other.distance:
            self._nodes.union(other)
            return
        return NotImplemented


class CachedDistanceGraph(DistanceGraph):
    r"""
    Graph of nodes connected by a cached distance function

    Compared to :py:class:`~DistanceGraph`, each edge is computed only once and
    stored for future lookup. Edges can be "deleted", which sets their value to
    an infinite value.

    :param nodes: all nodes contained in the graph
    :param distance: a function `dist(a, b)->object` that computes the distance between any two nodes
    :param undirected: whether distance can be treated as undirected, i.e. `dist(a, b) == dist(b, a)`

    :warning: For N nodes, all NxN edges are exposed and stored. This may lead
              to O(N\ :sup:2\ ) runtime and memory complexity.
    """
    def __init__(self, *source, **kwargs):
        super(CachedDistanceGraph, self).__init__(*source, **kwargs)
        self._distance_values = {}

    def __getitem__(self, item):
        # a:b -> slice -> edge
        if isinstance(item, slice):
            node_from, node_to = item.start, item.stop
            if node_from not in self._nodes:
                raise abc.EdgeError  # first edge node
            elif node_to not in self._nodes:
                raise abc.EdgeError  # second edge node
            # Since we don't know the type of nodes, we cannot test
            # node_to > node_from to detect swapped pairs. Since we
            # *do* store nodes in a `set`, they must support hash.
            if self.undirected and hash(node_to) > hash(node_from):
                node_to, node_from = node_from, node_to
            try:
                return self._distance_values[node_from, node_to]
            except KeyError:
                self._distance_values[node_from, node_to] = self.distance(node_from, node_to)
                return self._distance_values[node_from, node_to]
        else:
            return super(CachedDistanceGraph, self).__getitem__(item)

    def __delitem__(self, item):
        # a:b -> slice -> edge
        if isinstance(item, slice):
            node_from, node_to = item.start, item.stop
            if node_from not in self._nodes:
                raise abc.EdgeError  # first edge node
            elif node_to not in self._nodes:
                raise abc.EdgeError  # second edge node
            if self.undirected and hash(node_to) > hash(node_from):
                node_to, node_from = node_from, node_to
            self._distance_values[node_from, node_to] = self.maximum_distance
        else:
            try:
                self._nodes.remove(item)
            except KeyError:
                raise abc.NodeError
            else:
                # clean up all stored distances
                for node in self:
                    self._distance_values.pop((item, node), None)
                    if self.undirected:
                        continue
                    self._distance_values.pop((node, item), None)

    def clear(self):
        self._distance_values = type(self._distance_values)()
        super(CachedDistanceGraph, self).clear()
