#!/usr/bin/env python

import os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'
parent = os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))))

sys.path.insert(0, parent)

import django
from django.test.runner import DiscoverRunner
from django.conf import settings

settings.CRISPY_TEMPLATE_PACK = 'bootstrap3'


def runtests():
    if hasattr(django, 'setup'):
        django.setup()
    return DiscoverRunner(failfast=False).run_tests([
        'crispy_forms.tests.TestBasicFunctionalityTags',
        'crispy_forms.tests.TestFormHelper',
        'crispy_forms.tests.TestBootstrapFormHelper',
        'crispy_forms.tests.TestBootstrap3FormHelper',
        'crispy_forms.tests.TestFormLayout',
        'crispy_forms.tests.TestBootstrapFormLayout',
        'crispy_forms.tests.TestBootstrap3FormLayout',
        'crispy_forms.tests.TestLayoutObjects',
        'crispy_forms.tests.TestBootstrapLayoutObjects',
        'crispy_forms.tests.TestDynamicLayouts',
    ], verbosity=1, interactive=True)


if __name__ == '__main__':
    if runtests():
        sys.exit(1)
