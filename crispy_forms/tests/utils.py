__all__ = ('override_settings',)

from crispy_forms.compatibility import string_types
from django.utils.unittest import skipUnless

try:
    from django.test.utils import override_settings
except ImportError:
    # we are in Django 1.3
    from django.conf import settings, UserSettingsHolder
    from django.utils.functional import wraps

    class override_settings(object):
        """
        Acts as either a decorator, or a context manager. If it's a decorator
        it takes a function and returns a wrapped function. If it's a
        contextmanager it's used with the ``with`` statement. In either event
        entering/exiting are called before and after, respectively,
        the function/block is executed.

        This class was backported from Django 1.5

        As django.test.signals.setting_changed is not supported in 1.3,
        it's not sent on changing settings.
        """
        def __init__(self, **kwargs):
            self.options = kwargs
            self.wrapped = settings._wrapped

        def __enter__(self):
            self.enable()

        def __exit__(self, exc_type, exc_value, traceback):
            self.disable()

        def __call__(self, test_func):
            from django.test import TransactionTestCase
            if isinstance(test_func, type):
                if not issubclass(test_func, TransactionTestCase):
                    raise Exception(
                        "Only subclasses of Django SimpleTestCase "
                        "can be decorated with override_settings")
                original_pre_setup = test_func._pre_setup
                original_post_teardown = test_func._post_teardown

                def _pre_setup(innerself):
                    self.enable()
                    original_pre_setup(innerself)

                def _post_teardown(innerself):
                    original_post_teardown(innerself)
                    self.disable()
                test_func._pre_setup = _pre_setup
                test_func._post_teardown = _post_teardown
                return test_func
            else:
                @wraps(test_func)
                def inner(*args, **kwargs):
                    with self:
                        return test_func(*args, **kwargs)
            return inner

        def enable(self):
            override = UserSettingsHolder(settings._wrapped)
            for key, new_value in self.options.items():
                setattr(override, key, new_value)
            settings._wrapped = override

        def disable(self):
            settings._wrapped = self.wrapped


class OnlyIfTemplatePack(object):
    """
    This decorated is used to skip tests that are specific for just a specific
    template pack(s)
    """
    def __init__(self,template_pack_or_tuple):
        if isinstance(template_pack_or_tuple, string_types):
            self.template_packs = [template_pack_or_tuple,]
        else:
            self.template_packs = template_pack_or_tuple
    def __call__(self, func):
        decorator_self = self
        def wrapped( *args, **kwargs):
            from crispy_forms.layout import TEMPLATE_PACK
            return skipUnless(
                TEMPLATE_PACK in decorator_self.template_packs,
                'template pack is not in ' + repr(decorator_self.template_packs))(func)(*args, **kwargs)
        return wrapped


