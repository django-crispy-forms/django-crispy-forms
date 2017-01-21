from django.test.html import Element, parse_html


def contains_partial(haystack, needle):
    """Search for a html element with at least the corresponding elements
    (other elements may be present in the matched element from the haystack)
    """
    if not isinstance(haystack, Element):
        haystack = parse_html(haystack)
    if not isinstance(needle, Element):
        needle = parse_html(needle)

    if (
        needle.name == haystack.name and
        set(needle.attributes).issubset(haystack.attributes)
    ):
        return True
    return any(
        contains_partial(child, needle) for child in haystack.children
        if isinstance(child, Element)
    )
