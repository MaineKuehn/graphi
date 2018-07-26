try:
    import unittest2 as unittest
except ImportError:
    import unittest

from graphi.edge import Edge


class TestEdge(unittest.TestCase):
    def test_Init(self):
        self.assertEquals(Edge["start":"stop"], Edge("start", "stop"))

    def test_stop(self):
        with self.assertRaises(TypeError) as context:
            Edge["start":"stop":1]

    def test_slice(self):
        with self.assertRaises(TypeError) as context:
            Edge["start"]
