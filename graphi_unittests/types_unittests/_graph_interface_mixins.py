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
        def test_view_type(self):
            """Graph Interface: type(graph.nodes()), type(graph.edges()), ..."""
            with self.subTest(cls=self.graph_cls_identifier):
                graph = self.graph_cls()
                self.assertIsInstance(graph.nodes(), abc.NodeView)
                self.assertIsInstance(graph.edges(), abc.EdgeView)
                self.assertIsInstance(graph.values(), abc.ValueView)
                self.assertIsInstance(graph.items(), abc.ItemView)

        def test_node_views(self):
            """Graph Interface: node in graph.nodes(), iter(graph.nodes())"""
            with self.subTest(cls=self.graph_cls_identifier):
                graph = self.graph_cls(
                    {node_from: {
                        node_to: 1
                        for node_to in range(10, 20, 2)
                        if node_from < node_to
                    } for node_from in range(10, 20, 2)}
                )
                self.assertIn(10, graph.nodes())
                self.assertNotIn(1, graph.nodes())
                self.assertEqual(list(graph.nodes()), list(range(10, 20, 2)))
                self.assertEqual(len(graph.nodes()), len(list(graph.nodes())))

        def test_edge_views(self):
            """Graph Interface: edge in graph.edges(), iter(graph.edges())"""
            with self.subTest(cls=self.graph_cls_identifier):
                graph = self.graph_cls(
                    {node_from: {
                        node_to: 1
                        for node_to in range(10, 20, 2)
                        if node_from < node_to
                    } for node_from in range(10, 20, 2)}
                )
                self.assertIn(slice(10, 12), graph.edges())
                self.assertIn((10, 12), graph.edges())
                self.assertNotIn(slice(12, 10), graph.edges())
                self.assertNotIn((12, 10), graph.edges())
                with self.assertRaises(TypeError):
                    self.assertNotIn((10, 12, 14), graph.edges())
                self.assertEqual(len(graph.edges()), len(list(graph.edges())))

        def test_value_views(self):
            """Graph Interface: value in graph.values(), iter(graph.values())"""
            with self.subTest(cls=self.graph_cls_identifier):
                graph = self.graph_cls(
                    {node_from: {
                        node_to: 1
                        for node_to in range(10, 20, 2)
                        if node_from < node_to
                    } for node_from in range(10, 20, 2)}
                )
                self.assertIn(1, graph.values())
                self.assertNotIn(-1, graph.values())
                self.assertEqual(set(graph.values()), {1})
                self.assertEqual(len(graph.values()), len(list(graph.values())))

        def test_item_views(self):
            """Graph Interface: item in graph.items(), iter(graph.items())"""
            with self.subTest(cls=self.graph_cls_identifier):
                graph = self.graph_cls(
                    {node_from: {
                        node_to: 1
                        for node_to in range(10, 20, 2)
                        if node_from < node_to
                    } for node_from in range(10, 20, 2)}
                )
                self.assertIn((10, 12, 1), graph.items())
                self.assertNotIn((12, 10, 1), graph.items())
                self.assertNotIn((10, 12, -1), graph.items())
                with self.assertRaises(TypeError):
                    self.assertNotIn((10, 12, 14, 15), graph.items())
                    self.assertNotIn((10, 12), graph.items())
                self.assertEqual(len(graph.items()), len(list(graph.items())))

        def test_adjacency(self):
            """Graph Interface: item in graph.items(), iter(graph.items())"""
            with self.subTest(cls=self.graph_cls_identifier):
                graph = self.graph_cls(
                    {node_from: {
                        node_to: 1
                        for node_to in range(10, 20, 2)
                        if node_from < node_to
                    } for node_from in range(10, 20, 2)}
                )
                self.assertIn(12, graph[10])
                self.assertNotIn(10, graph[12])
                self.assertEqual(1, graph[10][12])
                self.assertEqual(len(graph[10]), len(list(graph[10])))
                self.assertNotIn(1, set(graph[10]))

        def test_node_container(self):
            """Graph Interface: bool(graph), len(graph), iter(graph) operate on nodes"""
            with self.subTest(cls=self.graph_cls_identifier):
                graph = self.graph_cls(iter(range(10, 20, 2)))
                self.assertTrue(graph)
                self.assertEqual(len(graph), len(range(10, 20, 2)))
                self.assertEqual(sorted(graph), sorted(range(10, 20, 2)))
                graph = self.graph_cls()
                self.assertFalse(graph)
                self.assertEqual(len(graph), 0)
                self.assertEqual(list(graph), [])

        def test_copy_clear_update(self):
            """Graph Interface: graph.copy(), graph.clear(), graph.update()"""
            with self.subTest(cls=self.graph_cls_identifier):
                for graph in (self.graph_cls(iter(range(10, 20, 2))), self.graph_cls()):
                    graph_copy = graph.copy()
                    self.assertIsNot(graph, graph_copy)
                    self.assertEqual(bool(graph), bool(graph_copy))
                    copy_bool = bool(graph_copy)
                    self.assertEqual(sorted(graph), sorted(graph_copy))
                    graph.clear()
                    self.assertFalse(bool(graph))
                    self.assertEqual(copy_bool, bool(graph_copy))
                    if copy_bool:
                        self.assertNotEqual(sorted(graph), sorted(graph_copy))
                    graph.update(iter(graph_copy))
                    self.assertIsNot(graph, graph_copy)
                    self.assertEqual(bool(graph), bool(graph_copy))
                    self.assertEqual(sorted(graph), sorted(graph_copy))

        def test_get_discard(self):
            """Graph Interface: graph.get(), graph.discard()"""
            with self.subTest(cls=self.graph_cls_identifier):
                nodes = list(range(10, 20, 2))
                graph = self.graph_cls(iter(nodes))
                for node in nodes:
                    self.assertIsNotNone(graph.get(node))
                    self.assertIsNone(graph.get(node + 1, default=None))
                for node in nodes:
                    self.assertIsNone(graph.discard(node))
                    self.assertIsNone(graph.discard(node + 1))

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

        def test_init_kwargs(self):
            """Graph Interface: graph(foobar=...)"""
            with self.subTest(cls=self.graph_cls_identifier):
                with self.assertRaises(TypeError):
                    self.graph_cls(foobar=12312)
                with self.assertRaises(TypeError):
                    self.graph_cls(foobar=12312, queras='foobar')
