import textwrap
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from graphi import abc
from graphi.graph_io import csv


class GraphIOTest(unittest.TestCase):
    @staticmethod
    def generate_matrix_csv(size=4, separator=',', undirected=False):
        """Create a matrix where each field corresponds to the difference between row and column"""
        literal = '\n'.join(
            separator.join(
                str(abs(rval - cval) if undirected is False else (cval - rval))
                for cval in range(size)
            )
            for rval in range(size)
        )
        return literal

    def test_default(self):
        """
        CSV GraphIO: using default settings

        string header, literals, any distance, ignore bool-False edges, undirected
        """
        literal = textwrap.dedent("""
        a,b,c,d
        0, 1,2,5
        1, 0,1,2
        2, 1,0,1
        5.2,16,None,5
        """.strip())
        graph = csv.graph_reader(literal.splitlines())
        # a row
        self.assertEqual(graph['a':'b'], 1)
        self.assertEqual(graph['a':'c'], 2)
        self.assertEqual(graph['a':'d'], 5)
        # b row
        self.assertEqual(graph['b':'a'], 1)
        self.assertEqual(graph['b':'c'], 1)
        self.assertEqual(graph['b':'d'], 2)
        # c row
        self.assertEqual(graph['c':'a'], 2)
        self.assertEqual(graph['c':'b'], 1)
        self.assertEqual(graph['c':'d'], 1)
        # d row
        self.assertEqual(graph['d':'a'], 5.2)
        self.assertEqual(graph['d':'b'], 16)
        self.assertEqual(graph['d':'d'], 5)
        # removed edges
        with self.assertRaises(abc.EdgeError):
            graph['a':'a']
        with self.assertRaises(abc.EdgeError):
            graph['b':'b']
        with self.assertRaises(abc.EdgeError):
            graph['c':'c']
        with self.assertRaises(abc.EdgeError):
            graph['d':'c']

    def test_invalid_header(self):
        """CSV GraphIO: invalid header"""
        literals = ["a,b", "0,1", "1,0"]
        with self.assertRaises(TypeError):
            csv.graph_reader(
                literals, nodes_header=None
            )
        literals = ["0,1", "1,0", "1,0", "0,1", "2,3"]
        with self.assertRaises(csv.ParserError):
            csv.graph_reader(literals, nodes_header=True)

    def test_header_none(self):
        """CSV GraphIO: default, enumerated header"""
        for undirected in (True, False):
            with self.subTest(undirected=undirected):
                for size in (1, 5, 10, 20):
                    literal = self.generate_matrix_csv(size, undirected=undirected)
                    graph = csv.graph_reader(
                        literal.splitlines(), nodes_header=False, undirected=undirected
                    )
                    self.assertHeaderMatrixGraph(list(range(size)), graph)

    def test_header_iterable(self):
        """CSV GraphIO: header from iterable"""
        for undirected in (True, False):
            with self.subTest(undirected=undirected):
                for size in (1, 5, 10, 20):
                    header = ['N%02d' % num for num in range(size)]
                    literal = self.generate_matrix_csv(size, undirected=undirected)
                    graph = csv.graph_reader(
                        literal.splitlines(), nodes_header=header, undirected=undirected
                    )
                    self.assertHeaderMatrixGraph(header, graph)

    def test_header_strings(self):
        """CSV GraphIO: header from first line as strings"""
        for undirected in (True, False):
            with self.subTest(undirected=undirected):
                for size in (1, 5, 10, 20):
                    header = ['N%02d' % num for num in range(size)]
                    literal = ','.join(header) + '\n' + self.generate_matrix_csv(size, undirected=undirected)
                    graph = csv.graph_reader(
                        literal.splitlines(), nodes_header=True, undirected=undirected
                    )
                    self.assertHeaderMatrixGraph(header, graph)

    def test_header_call(self):
        """CSV GraphIO: header from first line as strings"""
        for undirected in (True, False):
            with self.subTest(undirected=undirected):
                for size in (1, 5, 10, 20):
                    header = ['%2d' % num for num in range(size)]
                    literal = ','.join(header) + '\n' + self.generate_matrix_csv(size, undirected=undirected)
                    graph = csv.graph_reader(
                        literal.splitlines(), nodes_header=lambda elem: int(elem), undirected=undirected
                    )
                    self.assertHeaderMatrixGraph(list(range(size)), graph)

    def assertHeaderMatrixGraph(self, header, graph):
            self.assertEqual(sorted(graph), sorted(header))
            for row_idx, node_from in enumerate(header):
                for column_idx, node_to in enumerate(header):
                    if column_idx == row_idx:
                        with self.assertRaises(abc.EdgeError):
                            graph[node_from:node_to]
                    else:
                        self.assertEqual(graph[node_from:node_to], abs(column_idx - row_idx))

    def test_header_invalid(self):
        """CSV GraphIO: removed trailing empty line"""
        literal = textwrap.dedent("""
        a,b,c
        1,2,3
        4,5,6
        """.strip())
        graph = csv.graph_reader(literal.splitlines())
        # test defined edges
        self.assertEqual(graph['a':'a'], 1)
        self.assertEqual(graph['a':'b'], 2)
        self.assertEqual(graph['a':'c'], 3)
        self.assertEqual(graph['b':'a'], 4)
        self.assertEqual(graph['b':'b'], 5)
        self.assertEqual(graph['b':'c'], 6)
        # test undefined edges
        for target in "abc":
            with self.assertRaises(abc.EdgeError):
                graph['c':target]


class TestParserError(unittest.TestCase):
    def test_init(self):
        self.assertNotIn("column", str(csv.ParserError("test", 1)))
        self.assertIn("column", str(csv.ParserError("test", 1, 1)))
