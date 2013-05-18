# -*- coding: utf-8 -*-


def from_iterable(iterables):
    """
    Backport of `itertools.chain.from_iterable` compatible with Python 2.5
    """
    for it in iterables:
        for element in it:
            if isinstance(element, dict):
                for key in element:
                    yield key
            else:
                yield element


class KeepContext(object):
    """
    Context manager that receives a `django.template.Context` instance, tracks its changes
    and rolls them back when exiting the context manager, leaving the context unchanged.

    Layout objects can introduce context variables, that may cause side effects in later
    layout objects. This avoids that situation, without copying context every time.
    """
    def __init__(self, context):
        self.context = context

    def __enter__(self):
        self.old_set_keys = set(from_iterable(self.context.dicts))

    def __exit__(self, type, value, traceback):
        current_set_keys = set(from_iterable(self.context.dicts))
        diff_keys = current_set_keys - self.old_set_keys

        # We remove added keys for rolling back changes
        for key in diff_keys:
            self._delete_key_from_context(key)

    def _delete_key_from_context(self, key):
        for d in self.context.dicts:
            if key in d:
                del d[key]
