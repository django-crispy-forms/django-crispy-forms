# coding: utf-8
from django.conf import settings

import pytest

from .base import template_dirs, template_loaders


def get_skip_mark(*template_packs):
    return pytest.mark.skipif(settings.CRISPY_TEMPLATE_PACK not in template_packs,
                              reason='Requires %s template pack' % ' or '.join(template_packs))


only_uni_form = get_skip_mark('uni_form')
only_bootstrap = get_skip_mark('bootstrap', 'bootstrap3')
only_bootstrap3 = get_skip_mark('bootstrap3')


@pytest.fixture
def setup_templates(settings):
    settings.TEMPLATE_LOADERS = template_loaders
    settings.TEMPLATE_DIRS = template_dirs
