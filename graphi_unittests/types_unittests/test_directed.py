try:
    import unittest2 as unittest
except ImportError:
    import unittest

from graphi.types import undirected


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
