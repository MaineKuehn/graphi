try:
    import unittest2 as unittest
except ImportError:
    import unittest

from graphi.edge import Edge, Loop


class TestEdge(unittest.TestCase):
    def test_Init(self):
        self.assertEquals(Edge["start":"stop"], Edge("start", "stop"))

    def test_stop(self):
        with self.assertRaises(TypeError):
            Edge["start":"stop":1]

    def test_slice(self):
        with self.assertRaises(TypeError):
            Edge["start"]

    def test_index(self):
        edge = Edge("start", "stop")
        self.assertEquals(edge[0], "start")
        self.assertEquals(edge[1], "stop")
        with self.assertRaises(ValueError):
            edge[2]

    def test_iter(self):
        nodes = ["start", "stop"]
        edge = Edge(*nodes)

        for position, node in enumerate(edge):
            self.assertEquals(nodes[position], node)

        edge2 = Edge(*edge)
        self.assertEquals(edge2, edge)


class TestLoop(unittest.TestCase):
    def test_init(self):
        self.assertEquals(Loop("start"), Edge("start", "start"))
