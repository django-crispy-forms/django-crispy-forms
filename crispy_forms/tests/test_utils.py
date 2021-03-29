from django import forms
from django.template.base import Template
from django.template.context import Context
from django.test import SimpleTestCase

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.tests.utils import contains_partial
from crispy_forms.utils import list_difference, list_intersection, render_field

from .conftest import only_bootstrap4
from .forms import SampleForm
from .utils import parse_expected, parse_form


def test_list_intersection():
    assert list_intersection([1, 3], [2, 3]) == [3]


def test_list_difference():
    assert list_difference([3, 1, 2, 3], [4, 1]) == [3, 2]


def test_render_field_with_none_field():
    rendered = render_field(field=None, form=None, form_style=None, context=None)
    assert rendered == ""


def test_custom_bound_field():
    from django.forms.boundfield import BoundField

    extra = "xyxyxyxyxyx"

    class CustomBoundField(BoundField):
        @property
        def auto_id(self):
            return extra

    class MyCharField(forms.CharField):
        def get_bound_field(self, form, field_name):
            return CustomBoundField(form, self, field_name)

    class MyForm(forms.Form):
        f = MyCharField()

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.layout = Layout("f")

    template = Template('{% load crispy_forms_tags %}\n{% crispy form "bootstrap3" %}')
    rendered = template.render(Context({"form": MyForm(data={"f": "something"})}))

    assert extra in rendered


def test_contains_partial():
    c = SimpleTestCase()
    needle = "<span></span>"
    html = "<form>%s</form>"
    c.assertTrue(contains_partial(html % needle, needle))

    needle = "<span></span><b></b>"
    c.assertRaises(NotImplementedError, contains_partial, html % needle, needle)

    needle = "<span>a</span>"
    c.assertRaises(NotImplementedError, contains_partial, html % needle, needle)

    needle = '<span id="e"></span>'
    html = '<form id="tt"><span id="f"></span>%s</form>'
    c.assertTrue(contains_partial(html % needle, needle))

    missing = "<script></script>"
    c.assertFalse(contains_partial(html % missing, needle))

    needle = '<span id="e"></span>'
    html = '<form id="tt"><span id="f"></span>%s</form>'
    missing = '<span id="g"></span>'
    c.assertFalse(contains_partial(html % missing, needle))

    needle = '<div id="r"><span>toto</span></div>'
    html = '<form><div id="r"></div></form>'
    c.assertRaises(NotImplementedError, contains_partial, html, needle)
    # as we do not look at the children, needle is equivalent to <div id="r"></div> which IS in html
    c.assertTrue(contains_partial(html, needle, ignore_needle_children=True))


@only_bootstrap4
def test_parse_expected_and_form():
    form = SampleForm()
    form.helper = FormHelper()
    form.helper.layout = Layout("is_company")
    assert parse_form(form) == parse_expected("utils_test.html")
