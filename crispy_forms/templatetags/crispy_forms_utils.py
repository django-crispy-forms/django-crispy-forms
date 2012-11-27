# -*- coding: utf-8 -*-
import re

from django import template
from django.utils.encoding import force_unicode
from django.utils.functional import allow_lazy

register = template.Library()


def selectively_remove_spaces_between_tags(value):
    html = re.sub(r'>\s+<', '><', force_unicode(value))
    html = re.sub(r'</button><', '</button> <', force_unicode(html))
    return re.sub(r'(<input[^>]+>)<', r'\1 <', force_unicode(html))
selectively_remove_spaces_between_tags = allow_lazy(selectively_remove_spaces_between_tags, unicode)


class SpecialSpacelessNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        return selectively_remove_spaces_between_tags(
            self.nodelist.render(context).strip()
        )


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
