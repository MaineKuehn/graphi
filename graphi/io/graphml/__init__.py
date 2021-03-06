"""
Utilities for loading and storing Graphs as GraphML XML

The GraphML Format
------------------

This modules is capable of reading data according to the `GraphML Specification`_.
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
from .reader import graph_reader
