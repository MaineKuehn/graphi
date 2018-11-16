"""
Representations of the elements in a GraphML document
"""
import re


class QualifiedTag(object):
    """An XML tag consisting of (optional) namespace and local name"""
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
    """
    A GraphML Key specification on how to convert attributes of nodes

    :note: Unlike the GraphML ``key`` element, no domain is stored.
           See :py:class:`~.KeyDomain` for its equivalent.
    """
    types = {'boolean': bool, 'int': int, 'long': int, 'float': float, 'double': float, 'string': str}

    def __init__(self, identifier, attr_name, attr_type, default=None):
        if attr_type not in self.types:
            raise ValueError("'attr_type' must be any of '%s', not %s" % (
                "', '".join(self.types), identifier))
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
    """
    The GraphML domain to which keys apply

    A :py:class:`~.KeyDomain` represents all keys of a given domain.
    A GraphML ``key`` element with a ``domain`` is represented by a
    :py:class:`~.DataKey` stored in the corresponding :py:class:`~.KeyDomain`.
    """
    #: valid domains for GraphML keys
    GRAPHML_DOMAINS = "graph", "node", "edge", "all"

    def __init__(self, domain, keys):
        if domain not in self.GRAPHML_DOMAINS:
            raise ValueError("'domain' must be any of '%s', not %s" % (
                "', '".join(self.GRAPHML_DOMAINS), domain))
        self.domain = domain
        self.keys = tuple(keys)

    def compile_attributes(self, element):
        """
        Compile a dictionary of attributes from a graphml element for this domain

        :note: The validity of the domain is currently not checked.
               In the future, an error may be thrown if ``element`` is of the wrong domain.
        """
        attributes = {}
        child_data = {child.get('key'): child.text for child in element}
        for data_key in self.keys:  # type: DataKey
            try:
                value = child_data[data_key.identifier]
            except KeyError:
                # GraphML Primer:
                # If no default value is specified the value of the GraphML-Attribute
                # is undefined for the graph element [if it has no value].
                if data_key.default is not None:
                    attributes[data_key.attr_name] = data_key.default
            else:
                attributes[data_key.attr_name] = data_key.xml_to_py(value)
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
    """A GraphML node element"""
    def __init__(self, identifier, attributes):
        self.identifier = identifier
        self.attributes = attributes

    @classmethod
    def from_element(cls, element, key_domain):
        """Create a :py:class:`DataKey` instance from a graphml ``node`` element"""
        attributes = key_domain.compile_attributes(element)
        return cls(element.get('id'), attributes)


class GraphMLEdge(object):
    """A GraphML edge element"""
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


