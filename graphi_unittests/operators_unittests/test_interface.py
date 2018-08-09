try:
    import unittest2 as unittest
except ImportError:
    import unittest

from graphi.types import adjacency_graph
from graphi.operators import interface


class UnsupportedGraph(adjacency_graph.AdjacencyGraph):
    __graphi_operator__ = None


class UnoptimizedGraph(adjacency_graph.AdjacencyGraph):
    __graphi_operator__ = NotImplemented


class MaybeGraph(adjacency_graph.AdjacencyGraph):
    @staticmethod
    def __graphi_operator__(optimize=True):
        if optimize is False:
            return NotImplemented
        return 'maybe'


class OptimizedGraph(adjacency_graph.AdjacencyGraph):
    @staticmethod
    def __graphi_operator__():
        return 'optimized'


class TestInterface(unittest.TestCase):
    def test_decorator(self):
        """Bare operator protocol decorator"""
        @interface.graph_operator()
        def decorate_brackets(graph, *args, **kwargs):
            return 42

        @interface.graph_operator
        def decorate_bare(graph, *args, **kwargs):
            return 42

        for test_case in (decorate_brackets, decorate_bare):
            for test_subject in (object(), adjacency_graph.AdjacencyGraph()):
                with self.subTest(operator=test_case, subject=test_subject):
                    self.assertEqual(decorate_brackets(test_subject), 42)
                    self.assertEqual(decorate_brackets(test_subject, 73), 42)
                    self.assertEqual(decorate_brackets(test_subject, foo="bar"), 42)
                    self.assertEqual(decorate_brackets(test_subject, 21, foo="baz"), 42)

    def test_unsupported(self):
        """An operation is not supported by a graph"""
        @interface.graph_operator
        def operator(graph):
            return 0

        with self.assertRaises(TypeError):
            operator(UnsupportedGraph())

    def test_unoptimized(self):
        """An operation is not optimized by a graph"""
        @interface.graph_operator
        def operator(graph):
            return 0

        self.assertEqual(operator(UnoptimizedGraph()), 0)

    def test_maybe(self):
        """An operation is partially optimized by a graph"""
        @interface.graph_operator
        def operator(graph, optimize=True):
            return 0

        self.assertEqual(operator(MaybeGraph()), 'maybe')
        self.assertEqual(operator(MaybeGraph(), True), 'maybe')
        self.assertEqual(operator(MaybeGraph(), optimize=True), 'maybe')
        self.assertEqual(operator(MaybeGraph(), False), 0)
        self.assertEqual(operator(MaybeGraph(), optimize=False), 0)

    def test_optimized(self):
        """An operation is optimized by a graph"""
        @interface.graph_operator
        def operator(graph):
            return 0

        self.assertEqual(operator(OptimizedGraph()), 'optimized')
