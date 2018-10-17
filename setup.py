#!/usr/bin/env python
import os
import sys
import platform
from setuptools import setup, find_packages
from setuptools.extension import Extension

repo_base_dir = os.path.abspath(os.path.dirname(__file__))
# pull in the packages metadata
package_about = {}
with open(os.path.join(repo_base_dir, "graphi", "__about__.py")) as about_file:
    exec(about_file.read(), package_about)

with open(os.path.join(repo_base_dir, 'README.rst'), 'r') as README:
    long_description = README.read()

# setuptools.Extension automatically falls back to using .c files
# if Cython is not available to handle .pyx
CEXTENSIONS = [
    Extension(
        'graphi.types.cython_graph.plain_graph',
        ['graphi/types/cython_graph/plain_graph.pyx'],
    )
] if platform.python_implementation() == 'CPython' else []

install_requires = ['six']
if sys.version_info < (3, 4):
    install_requires.append('singledispatch')

if __name__ == '__main__':
    setup(
        name=package_about['__title__'],
        version=package_about['__version__'],
        description=package_about['__summary__'],
        long_description=long_description.strip(),
        author=package_about['__author__'],
        author_email=package_about['__email__'],
        url=package_about['__url__'],
        packages=find_packages(),
        # dependencies
        install_requires=install_requires,
        ext_modules=CEXTENSIONS,
        zip_safe=False,
        # metadata for package search
        license='MIT',
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Topic :: System :: Monitoring',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
        ],
        keywords=package_about['__keywords__'],
        # unit tests
        test_suite='graphi_unittests',
        # use unittest backport to have subTest etc.
        tests_require=['unittest2'] if sys.version_info < (3, 4) else [],
    )
