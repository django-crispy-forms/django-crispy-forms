# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from crispy_forms.utils import list_union, list_difference, list_intersection, set_hidden, render_field


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
