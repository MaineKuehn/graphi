import collections as abc_collection

from .. import abc
from .adjacency_graph import AdjacencyGraph


class Bounded(abc.Graph):
    @property
    def undirected(self):
        return self._graph.undirected

    def __init__(self, *source, **kwargs):
        self.value_bound = kwargs.pop('value_bound')
        self._graph = AdjacencyGraph()
        super(Bounded, self).__init__(*source, **kwargs)
        self._ensure_bounds()

    # initialize a new graph by copying nodes, edges and values from another graph
    def __init_graph__(self, graph, **kwargs):
        # TODO: copy graph?
        self._graph = graph
        super(Bounded, self).__init_graph__(graph, **kwargs)

    # initialize a new graph by copying nodes from an iterable
    def __init_iterable__(self, iterable, **kwargs):
        self._graph.update(iterable)
        super(Bounded, self).__init_iterable__(iterable, **kwargs)

    # initialize a new graph by copying nodes, edges and values from a nested mapping
    def __init_mapping__(self, mapping, **kwargs):
        self._graph.update(mapping)
        super(Bounded, self).__init_mapping__(mapping, **kwargs)

    def _ensure_bounds(self):
        blacklist = []
        for tail, head, value in self.items():
            if value > self.value_bound:
                blacklist.append((tail, head))
        if self.undirected:
            blacklist = {{tail, head} for tail, head in blacklist}
        for tail, head in blacklist:
            del self._graph[tail:head]

    def __getitem__(self, item):
        return self._graph[item]

    def __setitem__(self, item, value):
        # do not add edges exceeding our maximum distance
        if isinstance(item, slice) and value > self.value_bound:
            return
        elif isinstance(value, abc_collection.Mapping):
            value = {node: value for node, value in value.items() if value <= self.value_bound}
        super(Bounded, self).__setitem__(item, value)

    def __delitem__(self, item):
        del self._graph[item]

    def __iter__(self):
        return iter(self._graph)

    def __len__(self):
        return len(self._graph)

    def __bool__(self):
        return bool(self._graph)

    __nonzero__ = __bool__

    def __contains__(self, item):
        return item in self._graph

    def update(self, other):
        if isinstance(other, (abc.Graph, abc_collection.Mapping)):
            try:
                other_bound = getattr(other, 'value_bound')
            except AttributeError:
                other = Bounded(other, value_bound=self.value_bound)
            else:
                try:
                    if other_bound > self.value_bound:
                        other = Bounded(other, value_bound=self.value_bound)
                except TypeError as err:
                    raise ValueError('cannot update with bounds %r and %r: %s' % (self.value_bound, other_bound, err))
        self._graph.update(other)

    def clear(self):
        self._graph = type(self._graph)()
