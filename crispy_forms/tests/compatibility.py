# coding: utf-8


try:
    from django.template.loader import get_template_from_string
except ImportError:
    from django.template import Engine

    get_template_from_string = Engine.get_default().from_string
