#!/usr/bin/env python

import os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'
parent = os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))))

sys.path.insert(0, parent)

import django
from django.test.simple import DjangoTestSuiteRunner
from django.conf import settings

settings.CRISPY_TEMPLATE_PACK = 'bootstrap'


def runtests():
    if hasattr(django, 'setup'):
        django.setup()
    return DjangoTestSuiteRunner(failfast=False).run_tests([
        'crispy_forms.TestBasicFunctionalityTags',
        'crispy_forms.TestFormHelper',
        'crispy_forms.TestBootstrapFormHelper',
        'crispy_forms.TestFormLayout',
        'crispy_forms.TestBootstrapFormLayout',
        'crispy_forms.TestLayoutObjects',
        'crispy_forms.TestBootstrapLayoutObjects',
        'crispy_forms.TestDynamicLayouts',
    ], verbosity=1, interactive=True)


if __name__ == '__main__':
    if runtests():
        sys.exit(1)
