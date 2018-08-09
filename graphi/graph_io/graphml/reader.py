from xml.etree import ElementTree

from ...types import adjacency_graph
from .elements import KeyDomain, QualifiedTag, GraphMLNode, GraphMLEdge


class Namespace(object):
    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

    def __bool__(self):
        return bool(self.__dict__)

    def __eq__(self, other):
        if isinstance(other, Namespace):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.__dict__)


def true_namespace_value(edge):
    """All existing edges have either a ``True`` value or a namespace if any attributes are set"""
    if edge.attributes:
        return Namespace(**edge.attributes)
    return True


def id_node(node):
    """Create nodes from their ``id`` field"""
    return node.identifier


def graph_reader(source, node_type=id_node, value_type=true_namespace_value):
    try:
        graphml = ElementTree.fromstring(source)
    except ElementTree.ParseError:
        graphml = ElementTree.parse(source).getroot()
    node_key_domain = KeyDomain.from_graphml(domain='node', graphml=graphml)
    edge_key_domain = KeyDomain.from_graphml(domain='edge', graphml=graphml)
    for element in graphml:
        namespace, localname = QualifiedTag.from_tag(element.tag)
        if localname == 'graph':
            yield _construct_graph(element, node_type, value_type, node_key_domain, edge_key_domain)


def _construct_graph(graph_element, node_type, value_type, node_key_domain, edge_key_domain):
    default_directed = graph_element.get('edgedefault', None)
    nodes, edges = {}, {}
    for element in graph_element:
        namespace, localname = QualifiedTag.from_tag(element.tag)
        if localname == 'node':
            node = GraphMLNode.from_element(element, node_key_domain)
            nodes[node.identifier] = node_type(node)
        elif localname == 'edge':
            edge = GraphMLEdge.from_element(element, edge_key_domain, default_directed)
            edges[edge.identifier] = (edge, value_type(edge))
    graph = adjacency_graph.AdjacencyGraph(nodes.values())
    for edge, value in edges.values():
        graph[nodes[edge.source]:nodes[edge.target]] = value
    return graph
