import sys
try:
    basestring
except:
    basestring = str  # Python3

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
    # avoid RemovedInDjango19Warning by using lru_cache where available
    from django.utils.lru_cache import lru_cache
    def memoize(function, *args):
        return lru_cache()(function)
except:
    from django.utils.functional import memoize
