try:
    import unittest2 as unittest
except ImportError:
    import unittest

from graphi.abc import EdgeError
from graphi.types import bounded, adjacency_graph


class TestUndirected(unittest.TestCase):
    graph_cls = adjacency_graph.AdjacencyGraph

    def test_edges(self):
        graph = self.graph_cls({
            1: {2: 1, 3: 2, 4: 1}
        }, undirected=True, value_bound=1)
        self.assertIn(slice(1, 2), graph)
        self.assertNotIn(slice(1, 3), graph)
        self.assertNotIn(slice(2, 5), graph)
        graph[1:2] = 2
        with self.assertRaises(EdgeError):
            graph[1:2]

    def test_containment(self):
        graph = self.graph_cls(value_bound=1)
        self.assertFalse(bool(graph), "Graph is expected to be false as no nodes/edges are contained")
        self.assertEqual(len(graph), 0)
        graph.add(1)
        graph.add(2)
        graph[1:2] = 1
        self.assertTrue(bool(graph))
        self.assertEqual(len(graph), 2)

    def test_update(self):
        graph = adjacency_graph.AdjacencyGraph({
            1: {2: 2, 3: 1},
            2: {1: 2},
            3: {1: 1}
        })
        bounded_graph = bounded.Bounded({
            1: {3: 1, 4: 1}
        }, value_bound=1)
        bounded_graph.update(graph)
        self.assertIn(slice(1, 3), bounded_graph)
        self.assertIn(slice(1, 4), bounded_graph)
        self.assertNotIn(slice(1, 2), bounded_graph)
        self.assertNotIn(slice(2, 1), bounded_graph)
