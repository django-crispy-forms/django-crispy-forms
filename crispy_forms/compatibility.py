import django


if django.VERSION < (3, 0):
    from django.utils.lru_cache import lru_cache
else:
    from functools import lru_cache
