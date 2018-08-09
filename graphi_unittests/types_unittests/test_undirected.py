import textwrap
import unittest

from graphi.graph_io import csv

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
        self.assertEqual(len(graph), 0)
        graph.add(1)
        graph.add(2)
        graph[1:2] = 1
        self.assertTrue(bool(graph))
        self.assertEqual(len(graph), 2)

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
        second_graph = self.graph_cls({
            2: {3: 1}
        })
        undirected_graph.update(second_graph)
        self.assertIn(undirected.UndirectedEdge[2:3], undirected_graph)

    def test_conversion(self):
        literal = textwrap.dedent("""
                1,2,3,4,5,6,7,8
                0,1,1,1,1,2,0,1
                1,0,0,0,0,0,0,0
                1,0,0,0,0,0,0,0
                1,0,0,0,0,0,0,0
                1,0,0,0,0,0,0,0
                2,0,0,0,0,0,1,0
                0,0,0,0,0,1,0,0
                1,0,0,0,0,0,0,0
                """.strip())
        graph = csv.graph_reader(literal.splitlines(), undirected=True)
        self.assertTrue(slice("6", "1") in graph)
        self.assertTrue(graph.undirected)
        al_graph = adjacency_graph.AdjacencyGraph(graph)
        self.assertTrue(slice("6", "1") in al_graph)
        self.assertFalse(al_graph.undirected)
        clone_undirected = adjacency_graph.AdjacencyGraph(graph, undirected=True)
        self.assertTrue(slice("6", "1") in clone_undirected)
        self.assertTrue(clone_undirected.undirected)
        clone_bounded = adjacency_graph.AdjacencyGraph(graph, value_bound=1, undirected=True)
        self.assertTrue(slice("2", "1") in clone_bounded)
        self.assertFalse(slice("6", "1") in clone_bounded)
