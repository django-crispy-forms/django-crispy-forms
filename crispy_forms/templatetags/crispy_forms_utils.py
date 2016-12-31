# -*- coding: utf-8 -*-
import re

from django import template
from django.utils.encoding import force_text

try:
    from django.utils.functional import keep_lazy
except ImportError:
    # Django < 1.10
    from django.utils.functional import allow_lazy as keep_lazy

from crispy_forms.compatibility import text_type


register = template.Library()


def remove_spaces(value):
    html = re.sub(r'>\s{3,}<', '> <', force_text(value))
    return re.sub(r'/><', r'/> <', force_text(html))


remove_spaces = keep_lazy(remove_spaces, text_type)


class SpecialSpacelessNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        return remove_spaces(self.nodelist.render(context).strip())


@register.tag
def specialspaceless(parser, token):
    """
    Removes whitespace between HTML tags, and introduces a whitespace
    after buttons an inputs, necessary for Bootstrap to place them
    correctly in the layout.
    """
    nodelist = parser.parse(('endspecialspaceless',))
    parser.delete_first_token()

    return SpecialSpacelessNode(nodelist)
