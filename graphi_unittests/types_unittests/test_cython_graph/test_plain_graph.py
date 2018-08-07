import platform
try:
    import unittest2 as unittest
except ImportError:
    import unittest

try:
    from graphi.types.cython_graph.plain_graph import CythonGraph
except ImportError as err:
    class CythonGraph(object):
        failure_reason = str(err)

        def __new__(cls, *args, **kwargs):
            raise ImportError(cls.failure_reason)
    del err

from graphi_unittests.types_unittests import _graph_interface_mixins as mixins


@unittest.skipIf(platform.python_implementation() != 'CPython', 'Cython extension not available outside of CPython')
class TestCythonGraphInterface(mixins.Mixin.GraphInitMixin, mixins.Mixin.GraphInterfaceMixin):
    graph_cls = CythonGraph
