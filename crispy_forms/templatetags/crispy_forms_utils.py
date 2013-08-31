# -*- coding: utf-8 -*-
import re

from django import template
from django.conf import settings
try:  # Django < 1.4
    from django.utils.encoding import force_unicode as force_text
except ImportError:
    from django.utils.encoding import force_text
from django.utils.functional import allow_lazy

from crispy_forms.compatibility import text_type

register = template.Library()
TEMPLATE_PACK = getattr(settings, 'CRISPY_TEMPLATE_PACK', 'bootstrap')


def selectively_remove_spaces_between_tags(value, template_pack, form_class):
    if (
        'bootstrap' in template_pack
        and 'form-inline' in form_class
    ):
        # Bootstrap inline forms rely on spaces separating inputs, really
        html = re.sub(r'>\s+<', '> <', force_text(value))
        html = re.sub(r'</button><', '</button> <', force_text(html))
        return re.sub(r'/><', r'/> <', force_text(html))
    else:
        html = re.sub(r'>\s+<', '><', force_text(value))
        html = re.sub(r'</button><', '</button> <', force_text(html))
        return re.sub(r'/><', r'/> <', force_text(html))
    return value
selectively_remove_spaces_between_tags = allow_lazy(
    selectively_remove_spaces_between_tags, text_type
)


class SpecialSpacelessNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        try:
            template_pack = template.Variable('template_pack').resolve(context)
        except:
            template_pack = TEMPLATE_PACK

        try:
            form_attrs = template.Variable('form_attrs').resolve(context)
        except:
            form_attrs = {}

        return selectively_remove_spaces_between_tags(
            self.nodelist.render(context).strip(),
            template_pack,
            form_attrs.get('class', ''),
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
