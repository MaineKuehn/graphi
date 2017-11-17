import random
import itertools

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from graphi.types import adjacency_graph
from graphi.operators import density


class TestDensity(unittest.TestCase):
    def test_operator(self):
        """Operator density(complete_graph)"""
        for size in (2, 10, 100, random.randint(3, 9), random.randint(11, 19)):
            g = adjacency_graph.AdjacencyGraph(range(size))
            max_edges = size * (size - 1) * 1.0
            # one direction
            for count, (a, b) in enumerate(itertools.combinations(g, 2), 1):
                g[a:b] = True
                if count < 5 or 2 * count > max_edges - 6:
                    self.assertAlmostEqual(density(g), count / max_edges)
            self.assertEqual(density(g), 0.5)
            # any direction
            for count, (a, b) in enumerate(itertools.combinations(g, 2), 1):
                g[b:a] = True
                if count < 5 or 2 * count > max_edges - 6:
                    self.assertAlmostEqual(density(g), 0.5 + count / max_edges)
            self.assertEqual(density(g), 1)
            # self loops
            for count, a in enumerate(g, 1):
                g[a:a] = True
                if count < 5 or count > size - 5:
                    self.assertAlmostEqual(density(g), 1 + count / max_edges)
        # invalid cases
        with self.assertRaises(ValueError):
            # empty graph
            density(adjacency_graph.AdjacencyGraph())
        with self.assertRaises(ValueError):
            # single node
            density(adjacency_graph.AdjacencyGraph(1))
