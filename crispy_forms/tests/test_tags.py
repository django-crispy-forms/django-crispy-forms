# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.forms.forms import BoundField
from django.forms.models import formset_factory
from django.template import Context

import pytest

from .compatibility import get_template_from_string
from .conftest import only_bootstrap
from .forms import TestForm
from crispy_forms.templatetags.crispy_forms_field import crispy_addon


def test_as_crispy_errors_form_without_non_field_errors():
    template = get_template_from_string("""
        {% load crispy_forms_tags %}
        {{ form|as_crispy_errors }}
    """)
    form = TestForm({'password1': "god", 'password2': "god"})
    form.is_valid()

    c = Context({'form': form})
    html = template.render(c)
    assert not ("errorMsg" in html or "alert" in html)


def test_as_crispy_errors_form_with_non_field_errors():
    template = get_template_from_string("""
        {% load crispy_forms_tags %}
        {{ form|as_crispy_errors }}
    """)
    form = TestForm({'password1': "god", 'password2': "wargame"})
    form.is_valid()

    c = Context({'form': form})
    html = template.render(c)
    assert "errorMsg" in html or "alert" in html
    assert "<li>Passwords dont match</li>" in html
    assert "<h3>" not in html


def test_crispy_filter_with_form():
    template = get_template_from_string("""
        {% load crispy_forms_tags %}
        {{ form|crispy }}
    """)
    c = Context({'form': TestForm()})
    html = template.render(c)

    assert "<td>" not in html
    assert "id_is_company" in html
    assert html.count('<label') == 7


def test_crispy_filter_with_formset():
    template = get_template_from_string("""
        {% load crispy_forms_tags %}
        {{ testFormset|crispy }}
    """)

    TestFormset = formset_factory(TestForm, extra=4)
    testFormset = TestFormset()

    c = Context({'testFormset': testFormset})
    html = template.render(c)

    assert html.count('<form') == 0
    # Check formset management form
    assert 'form-TOTAL_FORMS' in html
    assert 'form-INITIAL_FORMS' in html
    assert 'form-MAX_NUM_FORMS' in html


def test_classes_filter():
    template = get_template_from_string("""
        {% load crispy_forms_field %}
        {{ testField|classes }}
    """)

    test_form = TestForm()
    test_form.fields['email'].widget.attrs.update({'class': 'email-fields'})
    c = Context({'testField': test_form.fields['email']})
    html = template.render(c)
    assert 'email-fields' in html


def test_crispy_field_and_class_converters():
    template = get_template_from_string("""
        {% load crispy_forms_field %}
        {% crispy_field testField 'class' 'error' %}
    """)
    test_form = TestForm()
    field_instance = test_form.fields['email']
    bound_field = BoundField(test_form, field_instance, 'email')

    c = Context({'testField': bound_field})
    html = template.render(c)
    assert 'error' in html
    assert 'inputtext' in html


@only_bootstrap
def test_crispy_addon(settings):
    test_form = TestForm()
    field_instance = test_form.fields['email']
    bound_field = BoundField(test_form, field_instance, 'email')

    if settings.CRISPY_TEMPLATE_PACK == 'bootstrap':
        # prepend tests
        assert "input-prepend" in crispy_addon(bound_field, prepend="Work")
        assert "input-append" not in crispy_addon(bound_field, prepend="Work")
        # append tests
        assert "input-prepend" not in crispy_addon(bound_field, append="Primary")
        assert "input-append" in crispy_addon(bound_field, append="Secondary")
        # prepend and append tests
        assert "input-append" in crispy_addon(bound_field, prepend="Work", append="Primary")
        assert "input-prepend" in crispy_addon(bound_field, prepend="Work", append="Secondary")
    elif settings.CRISPY_TEMPLATE_PACK == 'bootstrap3':
        assert "input-group-addon" in crispy_addon(bound_field, prepend="Work", append="Primary")
        assert "input-group-addon" in crispy_addon(bound_field, prepend="Work", append="Secondary")

    # errors
    with pytest.raises(TypeError):
        crispy_addon()
    with pytest.raises(TypeError):
        crispy_addon(bound_field)
