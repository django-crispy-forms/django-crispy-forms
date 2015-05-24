# -*- coding: utf-8 -*-
import os

from django.conf import settings
from django.template import loader
from django.test import TestCase

from crispy_forms.tests.utils import override_settings


class CrispyTestCase(TestCase):
    def setUp(self):
        template_dirs = [os.path.join(os.path.dirname(__file__), 'templates')]
        template_dirs = template_dirs + list(settings.TEMPLATE_DIRS)
        template_loaders = ['django.template.loaders.filesystem.Loader']
        template_loaders = template_loaders + list(settings.TEMPLATE_LOADERS)

        # ensuring test templates directory is loaded first
        self.__overriden_settings = override_settings(**{
            'TEMPLATE_LOADERS': template_loaders,
            'TEMPLATE_DIRS': template_dirs,
        })
        self.__overriden_settings.enable()


    def tearDown(self):
        pass

    @property
    def current_template_pack(self):
        return getattr(settings, 'CRISPY_TEMPLATE_PACK', 'bootstrap')
