import random

import graphi.types.adjacency_graph
import graphi.abc
from graphi import operators

try:
    import unittest2 as unittest
except ImportError:
    import unittest


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
        edge = graph[9]
        edge[2] = 2
        graph[9] = edge
        self.assertEqual(graph[9], {1: 1, 2: 2})

    def test_setitem_node(self):
        """Adjacency Graph: setitem of individual nodes"""
        graph = self.graph_cls(
            {idx: {} for idx in range(5)}
        )
        self.assertIn(1, graph)
        self.assertNotIn(5, graph)
        for null_edge in (len(graph), None):
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
