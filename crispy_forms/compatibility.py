import sys


PY2 = sys.version_info[0] == 2
if not PY2:
    text_type = str
    binary_type = bytes
    string_types = (str,)
    integer_types = (int,)
else:
    text_type = unicode
    binary_type = str
    string_types = basestring
    integer_types = (int, long)

try:
    from django.utils.lru_cache import lru_cache
except ImportError:
    from django.utils.functional import memoize as lru_cache
