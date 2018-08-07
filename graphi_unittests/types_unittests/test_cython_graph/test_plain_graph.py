try:
    import unittest2 as unittest
except ImportError:
    import unittest

try:
    from graphi.types.cython_graph.plain_graph import CythonGraph
except ImportError:
    CythonGraph = None

from . import _graph_interface_mixins as mixins


@unittest.skipIf(CythonGraph is None, 'Cython extension not available')
class TestCythonGraphInterface(mixins.Mixin.GraphInitMixin, mixins.Mixin.GraphInterfaceMixin):
    graph_cls = CythonGraph
