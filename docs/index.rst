.. graphi documentation master file, created by
   sphinx-quickstart on Wed Feb 22 14:45:32 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

+++++++++++++++++++++++++++++++++++++++++
GraphI - Python Graph Interface and Types
+++++++++++++++++++++++++++++++++++++++++


.. image:: https://landscape.io/github/MaineKuehn/graphi/master/landscape.svg?style=flat
    :target: https://landscape.io/github/MaineKuehn/graphi/master
    :alt: Code Health
.. image:: https://readthedocs.org/projects/graphi/badge/?version=latest
    :target: http://graphi.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. toctree::
    :maxdepth: 1
    :caption: Documentation Topics Overview:

    source/usage
    source/common_ops
    source/glossary
    Changelog <source/changelog>
    Module Index <source/api/modules>

``GraphI`` is a lightweight graph library - it is suitable to model networks, connections and other relationships.
Compared to other graph libraries, ``GraphI`` aims for being as pythonic as possible.
If you are comfortable using :py:class:`list`, :py:class:`dict` or other types, ``GraphI`` is intuitive and straight-forward to use.

.. code::

    from graphi.types.adjacency_graph import AdjacencyGraph
    # create a graph with initial nodes
    airports = AdjacencyGraph("New York", "Rio", "Tokyo")
    # add connections between nodes
    airports["New York":"Rio"] = timedelta(hours=9, minutes=50)
    airports["New York":"Tokyo"] = timedelta(hours=13, minutes=55)

At its heart, ``GraphI`` is built to integrate with Python's data model.
It natively works with primitives, iterables, mappings and whatever you need.
For example, creating a multigraph is as simple as using multiple edge values:

.. code::

    # add multiple connections between nodes -> Multigraph
    airports["Rio":"Tokyo"] = timedelta(days=1, hours=2), timedelta(days=1, hours=3)

By design, ``GraphI`` is primarily optimized for general convenience over specific brute force performance.
It heavily exploits lazy iteration, data views and other modern python paradigms under the hood.
This allows the use of common operations without loss of performance:

.. code::

    # get number of outgoing edges of nodes -> outdegree
    outgoing_flights = {city: len(airports[city]) for city in airports}

With its general-purpose design, ``GraphI`` makes no assumptions about your data.
You are free to use whatever is needed to solve your problem, not please data structure.

Frequently Asked Questions
==========================

*Yet another graph library?*
    The goal of ``GraphI`` is not to be another graph library, but to provide an intuitive way to work with graphs.
    Working with complex graphs should be as easy *for you* as working with any other primitive type.

*What is this thing you call ABC?*
    ``GraphI`` does not just provide graph *implementations*, but also an efficient graph *interface*.
    This interface is defined by the :py:class:`graphi.abc` :term:`abstract base classes <abstract base class>`.

    Any custom graph implementation can be made a *virtual* subclass of these ABCs.
    This allows you to adopt graph implementations optimized for your use-case without changing your code.

*Where are all the algorithms?*
    First and foremost, ``GraphI`` is designed for you to *work on graph data* instead of pre-sliced storybook data.
    ``GraphI`` implements only algorithms that

        1. are fundamental building blocks for advanced algorithms, and/or

        2. benefit from knowledge of internal data structures.

*What about performance?*
    At its core, ``GraphI`` uses Python's native, highly optimized data structures.
    For any non-trivial graph algorithm, the provided performance is more than sufficient.

    From our experience, performance critical code is best run with `PyPy <https://pypy.org>`_.
    This will not just optimize isolated pieces, but the actual combination of your algorithm and ``GraphI`` as a whole.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

----------

.. |issues| image:: https://img.shields.io/github/issues-raw/MaineKuehn/graphi.svg
   :target: https://github.com/MaineKuehn/graphi/issues
   :alt: Open Issues

Documentation built from graphi |version| at |today|.
