from . import abc
from .types import adjacency_graph

#: default graph implementation
graph = adjacency_graph.AdjacencyGraph

#: graph ABC/type
Graph = abc.Graph

__all__ = ['graph', 'Graph']
