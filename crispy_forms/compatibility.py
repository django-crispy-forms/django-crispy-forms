import sys

import django

if (1, 4) <= django.VERSION <= (1, 5):
    from django.utils.functional import SimpleLazyObject as DefaultSimpleLazyObject

    class SimpleLazyObject(DefaultSimpleLazyObject):

        def __contains__(self, item):
            if self._wrapped is None:
                self._setup()
            return self._wrapped.__contains__(item)
else:
    from django.utils.functional import SimpleLazyObject

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
except ImportError:
    from django.utils.functional import memoize

    def lru_cache():

        def decorator(function, cache_dict=None):
            if cache_dict is None:
                cache_dict = {}
            return memoize(function, cache_dict, 1)

        return decorator
