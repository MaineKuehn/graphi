from graphi import graph

from graphi_unittests.types_unittests import _graph_interface_mixins as mixins


class TestCythonPlainGraphInterface(mixins.Mixin.GraphInitMixin, mixins.Mixin.GraphInterfaceMixin):
    graph_cls = graph
