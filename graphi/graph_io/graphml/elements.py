"""
Utilities for loading and storing Graphs as GraphML XML

The GraphML Format
------------------

This modules is capable of reading data according to the `GraphML Specificiation`_.
The GraphML format covers all functionality that can be represented by :my:mod`graphi` graphs.
Note that several GraphML features, such as hyperedges, are not supported.

.. code:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <graphml xmlns="http://graphml.graphdrawing.org/xmlns"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns
         http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">
      <graph id="G" edgedefault="undirected">
        <node id="n0"/>
        <node id="n1"/>
        <node id="n2"/>
        <edge source="n0" target="n1"/>
        <edge source="n1" target="n2"/>
        <edge source="n2" target="n0"/>
      </graph>
    </graphml>

.. _`GraphML Specification`: http://graphml.graphdrawing.org/specification.html
"""
import re


class QualifiedTag(object):
    """A tag consisting of (optional) namespace and local name"""
    _literal_re = re.compile(r'({.*})?(.*)')

    def __init__(self, namespace, localname):
        self.namespace = namespace
        self.localname = localname

    def __iter__(self):
        return iter((self.namespace, self.localname))

    def __str__(self):
        if self.namespace is not None:
            return '{%s}%s' % self
        return self.localname

    @classmethod
    def from_tag(cls, tag):
        """Parse an ``{namespace}localname`` tag to a :py:class:`QualifiedTag`"""
        try:
            namespace, localname = cls._literal_re.match(tag).groups()
        except AttributeError:
            raise ValueError("tag %r is not a valid '{namespace}localname' literal")
        else:
            return cls(namespace, localname)


class DataKey(object):
    types = {'boolean': bool, 'int': int, 'long': int, 'float': float, 'double': float, 'string': str}

    def __init__(self, identifier, attr_name, attr_type, default=None):
        if attr_type not in self.types:
            raise ValueError("'attr_type' must be any of '%s'" % "', '".join(self.types))
        self.identifier = identifier
        self.attr_name = attr_name
        self.attr_type = attr_type
        self.xml_to_py = self.types[attr_type]
        self.default = default

    @classmethod
    def from_element(cls, element):
        """Create a :py:class:`DataKey` instance from a graphml ``key`` element"""
        attributes = element.attrib
        default = next(iter(element), None)
        return cls(
            identifier=attributes['id'], attr_name=attributes['attr.name'],
            attr_type=attributes['attr.type'], default=default,
        )


class KeyDomain(object):
    def __init__(self, domain, keys):
        self.domain = domain
        self.keys = tuple(keys)

    def compile_attributes(self, element):
        attributes = {}
        child_data = {child.get('key'): child.text for child in element}
        for data_key in self.keys:
            try:
                value = child_data[data_key.identifier]
            except KeyError:
                attributes[data_key.identifier] = data_key.default
            else:
                attributes[data_key.identifier] = data_key.xml_to_py(value)
        return attributes

    @classmethod
    def from_graphml(cls, domain, graphml):
        """Create a :py:class:`KeyDomain` instance for a given ``domain`` from a graphml root element"""
        keys = []
        for element in graphml:
            namespace, localname = QualifiedTag.from_tag(element.tag)
            if localname == 'key' and element.get('for', None) in (domain, 'all'):
                keys.append(DataKey.from_element(element))
        return cls(domain=domain, keys=keys)


class GraphMLNode(object):
    def __init__(self, identifier, attributes):
        self.identifier = identifier
        self.attributes = attributes

    @classmethod
    def from_element(cls, element, key_domain):
        """Create a :py:class:`DataKey` instance from a graphml ``node`` element"""
        attributes = key_domain.compile_attributes(element)
        return cls(element.get('id'), attributes)


class GraphMLEdge(object):
    def __init__(self, identifier, source, target, directed, attributes):
        self.identifier = identifier
        self.source = source
        self.target = target
        self.directed = directed
        self.attributes = attributes

    @classmethod
    def from_element(cls, element, key_domain, default_directed):
        """Create a :py:class:`DataKey` instance from a graphml ``edge`` element"""
        attributes = key_domain.compile_attributes(element)
        return cls(
            identifier=element.get('id'), source=element.get('source'), target=element.get('target'),
            directed=element.get('directed', default_directed), attributes=attributes
        )


