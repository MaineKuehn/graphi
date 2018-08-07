try:
    import unittest2 as unittest
except ImportError:
    import unittest

try:
    from graphi.types import _graph
except ImportError:
    _graph = None

from . import _graph_interface_mixins as mixins


@unittest.skipIf(_graph is None, 'Cython extension not available')
class TestCythonGraphInterface(mixins.Mixin.GraphInitMixin, mixins.Mixin.GraphInterfaceMixin):
    graph_cls = _graph.CythonGraph if _graph is not None else None
