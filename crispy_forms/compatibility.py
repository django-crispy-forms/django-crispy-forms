import django

if django.VERSION < (3, 0):
    from django.utils.lru_cache import lru_cache  # noqa: F401
else:
    from functools import lru_cache  # noqa: F401
