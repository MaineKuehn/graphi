import random
import unittest

from graphi.types import adjacency_graph
from graphi.operators import neighbours


class TestNeighbours(unittest.TestCase):
    @staticmethod
    def _get_edge_values():
        return [], [1, 2, 3, 4], [1, 2, 5, -3, 22, 42, -62, 21], [random.random() for _ in range(5)]

    def test_operator(self):
        """Operator neighbours(graph, node, ...)"""
        for edges in self._get_edge_values():
            with self.subTest(edges=edges):
                graph = adjacency_graph.AdjacencyGraph(
                    {'node': dict(enumerate(edges))}
                )
                # return all connected nodes - arbitrary order allowed
                self.assertEqual(set(neighbours(graph, 'node')), set(range(len(edges))))
                # return nodes up to a random element
                for start_val in edges + [0, 1, 10, float('inf')]:
                    self.assertEqual(
                        set(neighbours(graph, 'node', start_val)),
                        set(idx for idx, value in enumerate(edges) if value <= start_val)
                    )
                self.assertEqual(set(neighbours(graph, 'node', float('-inf'))), set())

    def test_override(self):
        """Overridden neighbours(graph, node, ...)"""
        class NeighboursGraph(adjacency_graph.AdjacencyGraph):
            pass

        @neighbours.register(NeighboursGraph)
        def test_neighbours(self, node, maximum_distance=None):
            if maximum_distance is None:
                return range(len(self[node]))
            if maximum_distance < 0:
                return []
            return range(int(maximum_distance))

        for edges in self._get_edge_values():
            with self.subTest(edges=edges):
                graph = NeighboursGraph(
                    {'node': dict(enumerate(edges))}
                )
                self.assertEqual(set(neighbours(graph, 'node')), set(range(len(edges))))
                self.assertEqual(set(neighbours(graph, 'node', -1)), set())
                self.assertEqual(set(neighbours(graph, 'node', 10)), set(range(10)))
