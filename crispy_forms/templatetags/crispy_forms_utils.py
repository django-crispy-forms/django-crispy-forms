from __future__ import annotations

import re
from typing import TYPE_CHECKING

from django import template
from django.utils.encoding import force_str
from django.utils.functional import keep_lazy

if TYPE_CHECKING:
    from django.template import Context
    from django.template.base import Parser, Token


register = template.Library()


@keep_lazy(str)
def remove_spaces(value: str) -> str:
    html = re.sub(r">\s{3,}<", "> <", force_str(value))
    return re.sub(r"/><", r"/> <", force_str(html))


class SpecialSpacelessNode(template.Node):
    def __init__(self, nodelist: template.NodeList) -> None:
        self.nodelist = nodelist

    def render(self, context: Context) -> str:
        return remove_spaces(self.nodelist.render(context).strip())


@register.tag
def specialspaceless(parser: Parser, token: Token) -> SpecialSpacelessNode:
    """
    Removes whitespace between HTML tags, and introduces a whitespace
    after buttons an inputs, necessary for Bootstrap to place them
    correctly in the layout.
    """
    nodelist = parser.parse(("endspecialspaceless",))
    parser.delete_first_token()

    return SpecialSpacelessNode(nodelist)
