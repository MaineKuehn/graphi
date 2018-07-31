+++++++++++++++++++++++++++++++++++++++++
GraphI - Python Graph Interface and Types
+++++++++++++++++++++++++++++++++++++++++

.. image:: https://readthedocs.org/projects/graphi/badge/?version=latest
    :target: http://graphi.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://travis-ci.org/MaineKuehn/graphi.svg?branch=master
    :target: https://travis-ci.org/MaineKuehn/graphi
    :alt: Test Status

.. image:: https://codecov.io/gh/MaineKuehn/graphi/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/MaineKuehn/graphi
    :alt: Test Coverage

.. image:: https://img.shields.io/pypi/v/graphi.svg
    :alt: Available on PyPI
    :target: https://pypi.python.org/pypi/graphi/

.. image:: https://img.shields.io/github/license/MaineKuehn/graphi.svg
    :alt: License
    :target: https://github.com/MaineKuehn/graphi/blob/master/LICENSE.txt

.. code:: python

    flighttime[berlin:london] = 3900
    # graph    node    node     value

``GraphI`` is a lightweight graph library - it is suitable to model networks, connections and other relationships.
Compared to other graph libraries, ``GraphI`` aims for being as pythonic as possible.
If you are comfortable using ``list``, ``dict`` or other types, ``GraphI`` is intuitive and straight-forward to use.

.. code:: python

    # create a graph with initial nodes
    airports = Graph("New York", "Rio", "Tokyo")
    # add connections between nodes
    airports["New York":"Rio"] = timedelta(hours=9, minutes=50)
    airports["New York":"Tokyo"] = timedelta(hours=13, minutes=55)

At its heart, ``GraphI`` is built to integrate with Python's data model.
It natively works with primitives, iterables, mappings and whatever you need.
For example, creating a multigraph can be as simple as using multiple edge values:

.. code:: python

    # add multiple connections between nodes
    airports["Rio":"Tokyo"] = timedelta(days=1, hours=2), timedelta(days=1, hours=3)

With its general-purpose design, ``GraphI`` makes no assumptions about your data.
You are free to use whatever is needed to solve your problem.

Getting started
===============

If you just want to use ``GraphI``, check out the `documentation <http://graphi.readthedocs.io/en/latest/?badge=latest>`_.

Development is hosted on `github <https://github.com/MaineKuehn/graphi>`_.
If you have issues or want to propose changes, check out the `issue tracker <https://github.com/MaineKuehn/graphi/issues>`_.
