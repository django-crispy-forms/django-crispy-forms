# coding: utf-8
import os
import sys


os.environ['DJANGO_SETTINGS_MODULE'] = 'crispy_forms.tests.test_settings'


for template_pack in ('uni_form', 'bootstrap', 'bootstrap3'):
    retval = os.system('CRISPY_TEMPLATE_PACK=%s py.test --cov=crispy_forms' % template_pack)
    if retval:
        sys.exit(1)
