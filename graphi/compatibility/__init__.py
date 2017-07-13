from __future__ import absolute_import
import sys

#: python version this module has been finalized for
compat_version = sys.version_info

inf = float('inf')

try:
    from .python3 import ABCBase
except SyntaxError:
    from .python2 import ABCBase
