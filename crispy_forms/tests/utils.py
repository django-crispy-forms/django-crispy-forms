import os
from pathlib import Path

from django.test.html import Element, parse_html

from crispy_forms.utils import render_crispy_form

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


def contains_partial(haystack, needle, ignore_needle_children=False):
    """Search for a html element with at least the corresponding elements
    (other elements may be present in the matched element from the haystack)
    """
    if not isinstance(haystack, Element):
        haystack = parse_html(haystack)
    if not isinstance(needle, Element):
        needle = parse_html(needle)

    if len(needle.children) > 0 and not ignore_needle_children:
        raise NotImplementedError("contains_partial does not check needle's children:%s" % str(needle.children))

    if needle.name == haystack.name and set(needle.attributes).issubset(haystack.attributes):
        return True
    return any(
        contains_partial(child, needle, ignore_needle_children=ignore_needle_children)
        for child in haystack.children
        if isinstance(child, Element)
    )


def parse_expected(expected_file):
    test_file = Path(TEST_DIR) / "results" / expected_file
    with test_file.open() as f:
        return parse_html(f.read())


def parse_form(form):
    html = render_crispy_form(form)
    return parse_html(html)
