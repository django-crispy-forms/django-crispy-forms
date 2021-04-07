from django import forms
from django.template.base import Template
from django.template.context import Context
from django.test import SimpleTestCase

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.templatetags.crispy_forms_filters import optgroups
from crispy_forms.tests.forms import GroupedChoiceForm, SampleForm5
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


def test_optgroup_filter_nested():
    form = GroupedChoiceForm({"checkbox_select_multiple": ["cd", "vhs"]})
    form.as_p()
    groups = optgroups(form["checkbox_select_multiple"])
    audio, video, unknown = groups
    label, options, index = audio
    assert label == "Audio"
    assert options == [
        {
            "value": "vinyl",
            "type": "checkbox",
            "attrs": {"id": "id_checkbox_select_multiple_0_0"},
            "index": "0_0",
            "label": "Vinyl",
            "template_name": "django/forms/widgets/checkbox_option.html",
            "name": "checkbox_select_multiple",
            "selected": False,
            "wrap_label": True,
        },
        {
            "value": "cd",
            "type": "checkbox",
            "attrs": {"checked": True, "id": "id_checkbox_select_multiple_0_1"},
            "index": "0_1",
            "label": "CD",
            "template_name": "django/forms/widgets/checkbox_option.html",
            "name": "checkbox_select_multiple",
            "selected": True,
            "wrap_label": True,
        },
    ]
    assert index == 0
    label, options, index = video
    assert label == "Video"
    assert options == [
        {
            "value": "vhs",
            "template_name": "django/forms/widgets/checkbox_option.html",
            "label": "VHS Tape",
            "attrs": {"checked": True, "id": "id_checkbox_select_multiple_1_0"},
            "index": "1_0",
            "name": "checkbox_select_multiple",
            "selected": True,
            "type": "checkbox",
            "wrap_label": True,
        },
        {
            "value": "dvd",
            "template_name": "django/forms/widgets/checkbox_option.html",
            "label": "DVD",
            "attrs": {"id": "id_checkbox_select_multiple_1_1"},
            "index": "1_1",
            "name": "checkbox_select_multiple",
            "selected": False,
            "type": "checkbox",
            "wrap_label": True,
        },
    ]
    assert index == 1
    label, options, index = unknown
    assert label is None
    assert options == [
        {
            "value": "unknown",
            "selected": False,
            "template_name": "django/forms/widgets/checkbox_option.html",
            "label": "Unknown",
            "attrs": {"id": "id_checkbox_select_multiple_2"},
            "index": "2",
            "name": "checkbox_select_multiple",
            "type": "checkbox",
            "wrap_label": True,
        }
    ]
    assert index == 2


def test_optgroup_filter():
    form = SampleForm5({"checkbox_select_multiple": "1"})
    groups = optgroups(form["checkbox_select_multiple"])
    group = groups[0]
    label, option, index = group
    assert label is None
    assert option == [
        {
            "name": "checkbox_select_multiple",
            "value": 1,
            "label": 1,
            "selected": True,
            "index": "0",
            "attrs": {"id": "id_checkbox_select_multiple_0", "checked": True},
            "type": "checkbox",
            "template_name": "django/forms/widgets/checkbox_option.html",
            "wrap_label": True,
        }
    ]
    assert index == 0

    form = SampleForm5({"checkbox_select_multiple": 1})
    groups = optgroups(form["checkbox_select_multiple"])
    group = groups[0]
    label, option, index = group
    assert label is None
    assert option == [
        {
            "name": "checkbox_select_multiple",
            "value": 1,
            "label": 1,
            "selected": True,
            "index": "0",
            "attrs": {"id": "id_checkbox_select_multiple_0", "checked": True},
            "type": "checkbox",
            "template_name": "django/forms/widgets/checkbox_option.html",
            "wrap_label": True,
        }
    ]
    assert index == 0

    form = SampleForm5({"checkbox_select_multiple": ""})
    groups = optgroups(form["checkbox_select_multiple"])
    group = groups[0]
    label, option, index = group
    assert label is None
    assert option == [
        {
            "name": "checkbox_select_multiple",
            "value": 1,
            "label": 1,
            "selected": False,
            "index": "0",
            "attrs": {"id": "id_checkbox_select_multiple_0"},
            "type": "checkbox",
            "template_name": "django/forms/widgets/checkbox_option.html",
            "wrap_label": True,
        }
    ]
    assert index == 0

    form = SampleForm5({"checkbox_select_multiple": None})
    groups = optgroups(form["checkbox_select_multiple"])
    group = groups[0]
    label, option, index = group
    assert label is None
    assert option == [
        {
            "name": "checkbox_select_multiple",
            "value": 1,
            "label": 1,
            "selected": False,
            "index": "0",
            "attrs": {"id": "id_checkbox_select_multiple_0"},
            "type": "checkbox",
            "template_name": "django/forms/widgets/checkbox_option.html",
            "wrap_label": True,
        }
    ]
    assert index == 0
