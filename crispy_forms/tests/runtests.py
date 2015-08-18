# coding: utf-8
import os
import sys


os.environ['DJANGO_SETTINGS_MODULE'] = 'crispy_forms.tests.test_settings'

base_tests = (
    'TestBasicFunctionalityTags',
    'TestFormHelper',
    'TestFormLayout',
    'TestLayoutObjects',
    'TestDynamicLayouts',
)
bootstrap_tests = base_tests + (
    'TestBootstrapFormHelper',
    'TestBootstrapFormLayout',
    'TestBootstrapLayoutObjects',
)
bootstrap_3_tests = bootstrap_tests + (
    'TestBootstrap3FormHelper',
    'TestBootstrap3FormLayout',
)
uni_form_tests = base_tests + (
    'TestUniformFormHelper',
    'TestUniformFormLayout',
    'TestUniformDynamicLayouts',
)


for template_pack, tests in (
        ('uni_form', uni_form_tests),
        ('bootstrap', bootstrap_tests),
        ('bootstrap3', bootstrap_3_tests)
):
    retval = os.system('CRISPY_TEMPLATE_PACK=%s py.test -k "%s"' % (template_pack, ' or '.join(tests)))
    if retval:
        sys.exit(1)
