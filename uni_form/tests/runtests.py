#!/usr/bin/env python

import os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'
parent = os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))))

sys.path.insert(0, parent)

from django.test.simple import DjangoTestSuiteRunner
from django.conf import settings

def runtests():
    DjangoTestSuiteRunner(failfast=False).run_tests([
        'uni_form.TestBasicFunctionalityTags',
        'uni_form.TestFormHelpers',
        'uni_form.TestFormLayout',
        ], verbosity=1, interactive=True)

if __name__ == '__main__':
    runtests()
