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
    Context manager that receives a `django.template.Context` instance and a list of keys

    Once the context manager is exited, it removes `keys` from the context, to avoid
    side effects in later layout objects that may use the same context variables.

    Layout objects should use `extra_context` to introduce context variables, never
    touch context object themselves, that could introduce side effects.
    """
    def __init__(self, context, keys):
        self.context = context
        self.keys = keys

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        for key in list(self.keys):
            del self.context[key]
