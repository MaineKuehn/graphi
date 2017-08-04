import itertools
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from graphi import abc
from graphi import edge
from graphi.types import adjacency_graph


class Mixin(object):
    """Container class to shield Mixins from top level namespace where ``unittest`` would run them"""
    class GraphMixin(unittest.TestCase):
        graph_cls = abc.Graph

        @staticmethod
        def _basic_nodes():
            return None, False, True, NotImplemented, '1', '2', 1, 2, 1.5, 2.5, -1

        @property
        def graph_cls_identifier(self):
            try:
                return '%s.%s' % (self.graph_cls.__module__, self.graph_cls.__qualname__)
            except AttributeError:
                return '%s.%s' % (self.graph_cls.__module__, self.graph_cls.__name__)

    class GraphInterfaceMixin(GraphMixin):
        def test_views(self):
            """Graph Interface: type(graph.nodes()), type(graph.edges()), ..."""
            with self.subTest(cls=self.graph_cls_identifier):
                graph = self.graph_cls()
                self.assertIsInstance(graph.nodes(), abc.NodeView)
                self.assertIsInstance(graph.edges(), abc.EdgeView)
                self.assertIsInstance(graph.values(), abc.ValueView)
                self.assertIsInstance(graph.items(), abc.ItemView)

    class GraphInitMixin(GraphMixin):
        def test_init_empty(self):
            """Graph Interface: graph()"""
            with self.subTest(cls=self.graph_cls_identifier):
                graph = self.graph_cls()
                # ensure the graph is empty
                for node in self._basic_nodes():
                    self.assertNotIn(node, graph)
                for a, b in itertools.product(self._basic_nodes(), repeat=2):
                    self.assertNotIn(edge.Edge[a:b], graph)
                self.assertEqual(len(graph), 0)
                self.assertEqual(len(graph.nodes()), 0)
                self.assertEqual(len(graph.edges()), 0)
                self.assertEqual(len(graph.values()), 0)
                self.assertEqual(len(graph.items()), 0)

        def test_init_iterable(self):
            """Graph Interface: graph(iter(...))"""
            with self.subTest(cls=self.graph_cls_identifier):
                graph = self.graph_cls(iter(range(10, 20, 2)))
                for node in range(10, 20, 2):
                    self.assertIn(node, graph)
                for a, b in itertools.product(range(10, 20, 2), repeat=2):
                    self.assertNotIn(edge.Edge[a:b], graph)
                self.assertEqual(len(graph), len(range(10, 20, 2)))
                self.assertEqual(len(graph.nodes()), len(range(10, 20, 2)))
                self.assertEqual(len(graph.edges()), 0)
                self.assertEqual(len(graph.values()), 0)
                self.assertEqual(len(graph.items()), 0)

        def test_init_variadic(self):
            """Graph Interface: graph(10, 12, ...)"""
            with self.subTest(cls=self.graph_cls_identifier):
                graph = self.graph_cls(*range(10, 20, 2))
                for node in range(10, 20, 2):
                    self.assertIn(node, graph)
                for a, b in itertools.product(range(10, 20, 2), repeat=2):
                    self.assertNotIn(edge.Edge[a:b], graph)
                self.assertEqual(len(graph), len(range(10, 20, 2)))
                self.assertEqual(len(graph.nodes()), len(range(10, 20, 2)))
                self.assertEqual(len(graph.edges()), 0)
                self.assertEqual(len(graph.values()), 0)
                self.assertEqual(len(graph.items()), 0)

        def test_init_adjacency(self):
            """Graph Interface: graph({a: {b: 1, c: 2}, b: ...})"""
            with self.subTest(cls=self.graph_cls_identifier):
                graph = self.graph_cls({
                    node_a: {
                        node_b: node_a - node_b for node_b in range(10, 20, 2)
                    } for node_a in range(10, 20, 2)
                })
                for node in range(10, 20, 2):
                    self.assertIn(node, graph)
                for a, b in itertools.product(range(10, 20, 2), repeat=2):
                    self.assertIn(edge.Edge[a:b], graph)
                    self.assertEqual(a - b, graph[a:b])
                self.assertEqual(len(graph), len(range(10, 20, 2)))
                self.assertEqual(len(graph.nodes()), len(range(10, 20, 2)))
                self.assertEqual(len(graph.edges()), len(range(10, 20, 2)) ** 2)
                self.assertEqual(len(graph.values()), len(range(10, 20, 2)) ** 2)
                self.assertEqual(len(graph.items()), len(range(10, 20, 2)) ** 2)

        def test_init_graph(self):
            """Graph Interface: graph(graph(...))"""
            with self.subTest(cls=self.graph_cls_identifier):
                graph = self.graph_cls(adjacency_graph.AdjacencyGraph({
                    node_a: {
                        node_b: node_a - node_b for node_b in range(10, 20, 2)
                    } for node_a in range(10, 20, 2)
                }))
                for node in range(10, 20, 2):
                    self.assertIn(node, graph)
                for a, b in itertools.product(range(10, 20, 2), repeat=2):
                    self.assertIn(edge.Edge[a:b], graph)
                    self.assertEqual(a - b, graph[a:b])
                self.assertEqual(len(graph), len(range(10, 20, 2)))
                self.assertEqual(len(graph.nodes()), len(range(10, 20, 2)))
                self.assertEqual(len(graph.edges()), len(range(10, 20, 2)) ** 2)
                self.assertEqual(len(graph.values()), len(range(10, 20, 2)) ** 2)
                self.assertEqual(len(graph.items()), len(range(10, 20, 2)) ** 2)
