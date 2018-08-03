import random

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import graphi.types.adjacency_graph
import graphi.abc
from graphi import operators
from graphi.types.decorator import undirectable

from . import _graph_interface_mixins as mixins


class TestAdjacencyGraphInterface(mixins.Mixin.GraphInitMixin, mixins.Mixin.GraphInterfaceMixin):
    graph_cls = graphi.types.adjacency_graph.AdjacencyGraph


@undirectable
class DistanceGraph(graphi.types.adjacency_graph.AdjacencyGraph):
    def __init__(self, *source, **kwargs):
        self.distance = kwargs.pop('distance', lambda a, b: 1)
        super(DistanceGraph, self).__init__(*source, **kwargs)

    def __getitem__(self, item):
        if isinstance(item, slice):
            assert item.step is None, '%s does not support stride argument for edges' % self.__class__.__name__
            node_from, node_to = item.start, item.stop
            if node_from not in self._adjacency:
                raise graphi.abc.EdgeError  # first edge node
            elif node_to not in self._adjacency:
                raise graphi.abc.EdgeError  # second edge node
            # Since we don't know the type of nodes, we cannot test
            # node_to > node_from to detect swapped pairs. Since we
            # *do* store nodes in a `set`, they must support hash.
            if self.undirected and hash(node_to) > hash(node_from):
                node_to, node_from = node_from, node_to
            return self.distance(node_from, node_to)
        else:
            if item not in self:
                raise graphi.abc.NodeError
            return {candidate: self[item:candidate] for candidate in self if candidate != item}


class TestAdjacencyGraph(unittest.TestCase):
    # distance graph class to test
    graph_cls = graphi.types.adjacency_graph.AdjacencyGraph

    @staticmethod
    def random_content(length, connections=None, distance_range=1.0):
        connections, have_connections = connections if connections is not None else length * length / 2, 0
        # create nodes
        adjacency = {random.randint(0, length * 10): {} for _ in range(length)}
        while len(adjacency) < length:  # postfix collisions
            adjacency[random.randint(0, length * 10)] = {}
        # connect nodes randomly
        nodes = list(adjacency)
        while have_connections < connections:
            for node in nodes:
                neighbour = random.choice(nodes)
                if neighbour not in adjacency[node]:
                    adjacency[node][neighbour] = random.random() * distance_range
                    adjacency[neighbour][node] = adjacency[node][neighbour]
                    have_connections += 1
        return adjacency

    def make_content_samples(self, lengths=range(5, 101, 20), connections=None, distance_range=1.0):
        yield {
            1: {2: 0.25},
            2: {1: 0.25, 3: 0.5},
            3: {2: 0.5, 4: 0.35},
            4: {3: 0.35}
        }  # fixed example
        connections = connections if connections is not None else [None] * len(lengths)
        for idx, length in enumerate(lengths):
            yield self.random_content(length, connections[idx], distance_range)

    def test_init_undirected(self):
        with self.assertRaises(ValueError):
            self.graph_cls({
                1: {2: 1, 3: 1},
                2: {1: 1},
                3: {1: 2}
            }, undirected=True)

        graph = self.graph_cls({
            1: {2: 1, 3: 1},
            2: {1: 1}
        }, undirected=True)
        self.assertEqual(graph[1:3], graph[3:1])

    def test_containment(self):
        """Adjacency Graph: retrieve elements"""
        graph = self.graph_cls({
            1: {2: 1, 3: 1, 4: 1, 5: 1, 6: 2, 8: 1},
            2: {1: 1},
            3: {1: 1},
            4: {1: 1},
            5: {1: 1},
            6: {1: 2, 7: 1},
            7: {6: 1},
            8: {1: 1}
        })
        self.assertEqual(1, graph[1:2])
        self.assertEqual(2, graph[6:1])
        with self.assertRaises(graphi.abc.EdgeError):
            graph[8:7]
        with self.assertRaises(graphi.abc.EdgeError):
            graph[9:10]
        self.assertEqual(graph[2], {1: 1})
        self.assertEqual(graph[6], {1: 2, 7: 1})
        self.assertEqual(graph[8], {1: 1})
        with self.assertRaises(graphi.abc.NodeError):
            graph[9]
        with self.assertRaises(graphi.abc.NodeError):
            graph[-1]
        with self.assertRaises(graphi.abc.NodeError):
            graph["notanode"]

    def test_set(self):
        """Adjacency Graph: change/add elements"""
        graph = self.graph_cls({
            1: {2: 1, 3: 1, 4: 1, 5: 1, 6: 2, 8: 1},
            2: {1: 1},
            3: {1: 1},
            4: {1: 1},
            5: {1: 1},
            6: {1: 2, 7: 1},
            7: {6: 1},
            8: {1: 1}
        }, undirected=True)
        self.assertFalse(slice(1, 7) in graph)
        graph[1:7] = 2
        self.assertEqual(2, graph[1:7])
        with self.assertRaises(graphi.abc.NodeError):
            graph[1:9] = 1
        with self.assertRaises(graphi.abc.NodeError):
            graph[9:1] = 1
        graph[9] = {}
        graph[9:1] = 1
        self.assertEqual(1, graph[1:9])
        edge = graph[9].copy()
        edge[2] = 2
        graph[9] = edge
        self.assertEqual(graph[9], {1: 1, 2: 2})
        graph[9] = {1: 1, 4: 5}
        self.assertEqual(graph[9], {1: 1, 4: 5})
        with self.assertRaises(graphi.abc.EdgeError):
            graph[2:9]
        with self.assertRaises(graphi.abc.AdjacencyListTypeError):
            graph[9] = None

    def test_setitem_node(self):
        """Adjacency Graph: setitem of individual nodes"""
        graph = self.graph_cls(
            {idx: {} for idx in range(5)}
        )
        self.assertIn(1, graph)
        self.assertNotIn(5, graph)
        null_edge = True
        for _ in range(len(graph) * 2):
            new_node = len(graph)
            with self.subTest(null_edge=null_edge, new_node=new_node, test='insert'):
                self.assertNotIn(new_node, graph)
                graph[new_node] = null_edge
                self.assertIn(new_node, graph)
                graph[new_node] = null_edge
                self.assertIn(new_node, graph)
                self.assertEqual(graph[new_node], {})
            edges = {1: 3, 2: 5}
            with self.subTest(null_edge=null_edge, new_node=new_node, test='set'):
                graph[new_node] = edges
                self.assertEqual(graph[new_node], edges)
                for node_to in edges:
                    self.assertEqual(graph[new_node:node_to], edges[node_to])
            with self.subTest(null_edge=null_edge, new_node=new_node, test='ensure'):
                graph[new_node] = null_edge
                self.assertEqual(graph[new_node], edges)
            with self.subTest(null_edge=null_edge, new_node=new_node, test='expand'):
                edges = graph[new_node]
                edges[4] = 99
                graph[new_node] = edges
                self.assertEqual(graph[new_node], edges.copy())
                for node_to in edges:
                    self.assertEqual(graph[new_node:node_to], edges[node_to])

    def test_deletion(self):
        graph = self.graph_cls({
            1: {2: 1, 3: 1, 4: 1, 5: 1, 6: 2, 8: 1},
            2: {1: 1},
            3: {1: 1},
            4: {1: 1},
            5: {1: 1},
            6: {1: 2, 7: 1},
            7: {6: 1},
            8: {1: 1}
        })
        with self.assertRaises(graphi.abc.EdgeError):
            del graph[1:7]
        self.assertEqual(1, graph[6:7])
        del graph[6]
        with self.assertRaises(graphi.abc.EdgeError):
            del graph[6:7]
        with self.assertRaises(graphi.abc.NodeError):
            del graph[6]
        del graph[8:1]
        with self.assertRaises(graphi.abc.EdgeError):
            graph[8:1]

    def test_deletion_undirected(self):
        graph = self.graph_cls({
            1: {2: 1, 3: 1, 4: 1},
            2: {1: 1},
            3: {1: 1},
            4: {1: 1}
        }, undirected=True)
        del graph[1:2]
        with self.assertRaises(graphi.abc.EdgeError):
            graph[1:2]
        with self.assertRaises(graphi.abc.EdgeError):
            graph[2:1]
        del graph[4]
        with self.assertRaises(graphi.abc.EdgeError):
            graph[1:4]
        with self.assertRaises(graphi.abc.EdgeError):
            graph[4:1]

    def test_neighbours(self):
        graph = self.graph_cls({
            1: {2: 1, 3: 1, 4: 1, 5: 1, 6: 2, 8: 1},
            2: {1: 1},
            3: {1: 1},
            4: {1: 1},
            5: {1: 1},
            6: {1: 2, 7: 1},
            7: {6: 1},
            8: {1: 1}
        })
        self.assertEqual({2, 3, 4, 5, 6, 8}, set(operators.neighbours(graph, 1)))
        self.assertEqual({2, 3, 4, 5, 8}, set(operators.neighbours(graph, 1, maximum_distance=1)))
        with self.assertRaises(graphi.abc.NodeError):
            operators.neighbours(graph, 9)

    def test_update(self):
        graph = self.graph_cls({
            1: {2: 1, 3: 1, 4: 1},
            2: {1: 1},
            3: {1: 1},
            4: {1: 1}
        }, undirected=True)
        graph.update((5, 6))
        self.assertIn(5, graph)
        self.assertIn(6, graph)

    def test_clear_undirected(self):
        graph = self.graph_cls({
            1: {2: 1, 3: 1, 4: 1},
            2: {1: 1},
            3: {1: 1},
            4: {1: 1}
        }, undirected=True)
        self.assertEqual(len(graph), 4)
        graph.clear()
        self.assertEqual(len(graph), 0)

    def test_clear_directed(self):
        graph = self.graph_cls({
            1: {2: 1, 3: 1, 4: 1},
            2: {1: 1},
            3: {1: 1},
            4: {1: 1}
        })
        self.assertEqual(len(graph), 4)
        graph.clear()
        self.assertEqual(len(graph), 0)

    def test_edge_view_undirected(self):
        graph = self.graph_cls({1, 2, 3, 4}, undirected=True)
        nodes = [2, 3, 4]
        for node in nodes:
            graph[1:node] = 1
        counter = 0
        edge_view = graph.edges()
        for edge in edge_view:
            self.assertTrue(edge in graph)
            self.assertTrue(edge in edge_view)
            counter += 1
        self.assertEqual(len(nodes), counter, "The number of edges should be half for undirected graphs")
        self.assertTrue(graphi.edge.Edge[1:2] in edge_view)
        self.assertFalse(graphi.edge.Edge[1:5] in edge_view)
        self.assertTrue([1, 2] in edge_view)
        self.assertFalse([1, 5] in edge_view)
        with self.assertRaises(TypeError):
            [1, 2, 3] in edge_view
        with self.assertRaises(TypeError):
            None in edge_view

    def test_edge_view_directed(self):
        graph = self.graph_cls({1, 2, 3, 4, 5})
        nodes = [2, 3, 4]
        for node in nodes:
            graph[1:node] = 1
            graph[node:1] = 1
        graph[1:5] = 1
        counter = 0
        edge_view = graph.edges()
        for edge in edge_view:
            self.assertTrue(edge in graph)
            self.assertTrue(edge in edge_view)
            counter += 1
        self.assertEqual(len(nodes) * 2 + 1, counter)
        self.assertTrue(graphi.edge.Edge[1:2] in edge_view)
        self.assertFalse(graphi.edge.Edge[5:1] in edge_view)
        self.assertTrue([1, 2] in edge_view)
        self.assertFalse([5, 1] in edge_view)
        with self.assertRaises(TypeError):
            [1, 2, 3] in edge_view
        with self.assertRaises(TypeError):
            None in edge_view

    def test_value_view_undirected(self):
        graph = self.graph_cls({1, 2, 3, 4}, undirected=True)
        nodes = [2, 3, 4]
        for value, node in enumerate(nodes):
            graph[1:node] = value
        value_view = graph.values()
        for value in value_view:
            self.assertIn(value, [0, 1, 2])
            self.assertTrue(value in value_view)
        self.assertFalse(3 in value_view)
        self.assertEqual(len(nodes), len(value_view), "The number of values should be half for undirected graphs")

    def test_value_view_directed(self):
        graph = self.graph_cls({1, 2, 3, 4})
        nodes = [2, 3, 4]
        for value, node in enumerate(nodes):
            graph[1:node] = value
            graph[node:1] = 4
        value_view = graph.values()
        for value in value_view:
            self.assertIn(value, [0, 1, 2, 4])
            self.assertTrue(value in value_view)
        self.assertFalse(3 in value_view)
        self.assertEqual(len(nodes) * 2, len(value_view))

    def test_graph_customisation(self):
        graph = DistanceGraph([1, 2], undirected=True)
        self.assertEqual(1, graph[1:2])
        self.assertEqual(1, graph.distance(1, 2))
