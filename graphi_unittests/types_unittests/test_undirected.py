try:
    import unittest2 as unittest
except ImportError:
    import unittest

from graphi.types import undirected, adjacency_graph


class TestUndirected(unittest.TestCase):
    graph_cls = undirected.Undirected

    def test_edges(self):
        graph = self.graph_cls({
            1: {2: 1, 3: 1, 4: 1}
        })
        last_edge = None
        for edge in graph.edges():
            self.assertEqual(edge, edge)
            self.assertNotEqual(last_edge, edge)
            last_edge = edge
        self.assertFalse(last_edge == [1])

    def test_containment(self):
        graph = self.graph_cls()
        self.assertFalse(bool(graph), "Graph is expected to be false as no nodes/edges are contained")
        self.assertEquals(len(graph), 0)
        graph.add(1)
        graph.add(2)
        graph[1:2] = 1
        self.assertTrue(bool(graph))
        self.assertEquals(len(graph), 2)

    def test_update(self):
        graph = adjacency_graph.AdjacencyGraph({
            1: {2: 1, 3: 1},
            2: {1: 1},
            3: {1: 1}
        })
        undirected_graph = self.graph_cls({
            1: {2: 1, 4: 1}
        })
        undirected_graph.update(graph)
        self.assertIn(undirected.UndirectedEdge[1:3], undirected_graph)
        self.assertIn(undirected.UndirectedEdge[1:4], undirected_graph)
        self.assertNotIn(undirected.UndirectedEdge[2:3], undirected_graph)
