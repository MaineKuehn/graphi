import sys
try:
    import unittest2 as unittest
    sys.modules['unittest'] = unittest
except ImportError:
    import unittest
