#!/usr/bin/env python

import os, sys, logging, warnings

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'
parent = os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))))

sys.path.insert(0, parent)

import django
from django.test.simple import DjangoTestSuiteRunner
from django.conf import settings
settings.CRISPY_TEMPLATE_PACK = 'uni_form'


def runtests():
    if hasattr(django, 'setup'):
        django.setup()
    return DjangoTestSuiteRunner(failfast=False).run_tests([
        'crispy_forms.TestBasicFunctionalityTags',
        'crispy_forms.TestFormHelper',
        'crispy_forms.TestUniformFormHelper',
        'crispy_forms.TestFormLayout',
        'crispy_forms.TestUniformFormLayout',
        'crispy_forms.TestLayoutObjects',
        'crispy_forms.TestDynamicLayouts',
        'crispy_forms.TestUniformDynamicLayouts',
    ], verbosity=1, interactive=True)


if __name__ == '__main__':
    if runtests():
        sys.exit(1)
