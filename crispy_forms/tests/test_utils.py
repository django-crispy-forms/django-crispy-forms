# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from crispy_forms.utils import list_union, list_difference, list_intersection, set_hidden, render_field
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
import django
from django import forms
from django.template.base import Context, Template
import pytest

def test_list_intersection():
    assert list_intersection([1, 3], [2, 3]) == [3]


def test_list_difference():
    assert list_difference([3, 1, 2, 3], [4, 1, ]) == [3, 2]


def test_list_set_operations():
    list1 = ['3', '1', '4', '3']
    list2 = ['2']
    list3 = ['1', '6']
    list4 = []
    union = list_union(list1, list2, list3, list4)
    assert union == ['3', '1', '4', '2', '6']
    list5 = ['1', '3']
    list6 = ['2', '3']
    difference = list_difference(list5, list6)
    assert difference == ['1']


def test_set_hidden():
    class FakeWidget(object):
        is_hidden = False

    widget = FakeWidget()
    set_hidden(widget)

    assert widget.is_hidden is True


def test_render_field_with_none_field():
    rendered = render_field(field=None, form=None, form_style=None, context=None)
    assert rendered == ''

@pytest.mark.skipif(django.VERSION < (1, 9),
                    reason="Custom BoundField behavior is was introduced in 1.9.")
def test_custom_bound_field():
    from django.forms.boundfield import BoundField

    extra = 'xyxyxyxyxyx'

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
            super(MyForm, self).__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.layout = Layout('f')

    template = Template('{% load crispy_forms_tags %}\n{% crispy form "bootstrap3" %}')
    rendered = template.render(Context({'form': MyForm(data={'f': 'something'})}))

    assert extra in rendered
