from ...abc import Graph as GraphABC
from ..decorator import boundable, undirectable

from .plain_graph import CythonGraph as _PlainGraph


@boundable
@undirectable
class CythonGraph(GraphABC):
    """
    Optimised Cython Graph Implementations

    .. note:: This is an abstract class that merely picks the most suitable implementation.
    """
    def __new__(cls, *args, **kwargs):
        return _PlainGraph(*args, **kwargs)


CythonGraph.register(_PlainGraph)
