# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

import pytest

import django
from django import forms
from django.forms.models import formset_factory
from django.template import Context, Template, TemplateSyntaxError
from django.test.html import parse_html
from django.utils.translation import ugettext_lazy as _

from crispy_forms.bootstrap import (
    AppendedText, FieldWithButtons, PrependedAppendedText, PrependedText,
    StrictButton,
)
from crispy_forms.compatibility import text_type
from crispy_forms.helper import FormHelper, FormHelpersException
from crispy_forms.layout import (
    Button, Field, Hidden, Layout, MultiField, Reset, Submit,
)
from crispy_forms.templatetags.crispy_forms_tags import CrispyFormNode
from crispy_forms.utils import render_crispy_form

from .conftest import (
    only_bootstrap, only_bootstrap3, only_bootstrap4, only_uni_form,
)
from .forms import SampleForm, SampleFormWithMedia, SampleFormWithMultiValueField

try:
    from django.middleware.csrf import _get_new_csrf_key
except ImportError:
    from django.middleware.csrf import _get_new_csrf_string as _get_new_csrf_key

try:
    from django.urls import reverse
except ImportError:
    # Django < 1.10
    from django.core.urlresolvers import reverse


def test_inputs(settings):
    form_helper = FormHelper()
    form_helper.add_input(Submit('my-submit', 'Submit', css_class="button white"))
    form_helper.add_input(Reset('my-reset', 'Reset'))
    form_helper.add_input(Hidden('my-hidden', 'Hidden'))
    form_helper.add_input(Button('my-button', 'Button'))

    template = Template("""
        {% load crispy_forms_tags %}
        {% crispy form form_helper %}
    """)
    c = Context({'form': SampleForm(), 'form_helper': form_helper})
    html = template.render(c)

    assert 'button white' in html
    assert 'id="submit-id-my-submit"' in html
    assert 'id="reset-id-my-reset"' in html
    assert 'name="my-hidden"' in html
    assert 'id="button-id-my-button"' in html

    if settings.CRISPY_TEMPLATE_PACK == 'uni_form':
        assert 'submit submitButton' in html
        assert 'reset resetButton' in html
        assert 'class="button"' in html
    else:
        assert 'class="btn"' in html
        assert 'btn btn-primary' in html
        assert 'btn btn-inverse' in html
        assert len(re.findall(r'<input[^>]+> <', html)) == 8


def test_invalid_form_method():
    form_helper = FormHelper()
    with pytest.raises(FormHelpersException):
        form_helper.form_method = "superPost"


def test_form_with_helper_without_layout(settings):
    form_helper = FormHelper()
    form_helper.form_id = 'this-form-rocks'
    form_helper.form_class = 'forms-that-rock'
    form_helper.form_method = 'GET'
    form_helper.form_action = 'simpleAction'
    form_helper.form_error_title = 'ERRORS'

    template = Template("""
        {% load crispy_forms_tags %}
        {% crispy testForm form_helper %}
    """)

    # now we render it, with errors
    form = SampleForm({'password1': 'wargame', 'password2': 'god'})
    form.is_valid()
    c = Context({'testForm': form, 'form_helper': form_helper})
    html = template.render(c)

    # Lets make sure everything loads right
    assert html.count('<form') == 1
    assert 'forms-that-rock' in html
    assert 'method="get"' in html
    assert 'id="this-form-rocks"' in html
    assert 'action="%s"' % reverse('simpleAction') in html

    if settings.CRISPY_TEMPLATE_PACK == 'uni_form':
        assert 'class="uniForm' in html

    assert "ERRORS" in html
    assert "<li>Passwords dont match</li>" in html

    # now lets remove the form tag and render it again. All the True items above
    # should now be false because the form tag is removed.
    form_helper.form_tag = False
    html = template.render(c)
    assert '<form' not in html
    assert 'forms-that-rock' not in html
    assert 'method="get"' not in html
    assert 'id="this-form-rocks"' not in html


def test_form_show_errors_non_field_errors():
    form = SampleForm({'password1': 'wargame', 'password2': 'god'})
    form.helper = FormHelper()
    form.helper.form_show_errors = True
    form.is_valid()

    template = Template("""
        {% load crispy_forms_tags %}
        {% crispy testForm %}
    """)

    # First we render with errors
    c = Context({'testForm': form})
    html = template.render(c)

    # Ensure those errors were rendered
    assert '<li>Passwords dont match</li>' in html
    assert text_type(_('This field is required.')) in html
    assert 'error' in html

    # Now we render without errors
    form.helper.form_show_errors = False
    c = Context({'testForm': form})
    html = template.render(c)

    # Ensure errors were not rendered
    assert '<li>Passwords dont match</li>' not in html
    assert text_type(_('This field is required.')) not in html
    assert 'error' not in html


def test_html5_required():
    form = SampleForm()
    form.helper = FormHelper()
    form.helper.html5_required = True
    html = render_crispy_form(form)
    # 6 out of 7 fields are required and an extra one for the SplitDateTimeWidget makes 7.
    if django.VERSION < (1, 10):
        assert html.count('required="required"') == 7
    else:
        assert len(re.findall(r'\brequired\b', html)) == 7


    form = SampleForm()
    form.helper = FormHelper()
    form.helper.html5_required = False
    html = render_crispy_form(form)


def test_media_is_included_by_default_with_uniform():
    form = SampleFormWithMedia()
    form.helper = FormHelper()
    form.helper.template_pack = 'uni_form'
    html = render_crispy_form(form)
    assert 'test.css' in html
    assert 'test.js' in html


def test_media_is_included_by_default_with_bootstrap():
    form = SampleFormWithMedia()
    form.helper = FormHelper()
    form.helper.template_pack = 'bootstrap'
    html = render_crispy_form(form)
    assert 'test.css' in html
    assert 'test.js' in html


def test_media_is_included_by_default_with_bootstrap3():
    form = SampleFormWithMedia()
    form.helper = FormHelper()
    form.helper.template_pack = 'bootstrap3'
    html = render_crispy_form(form)
    assert 'test.css' in html
    assert 'test.js' in html


def test_media_is_included_by_default_with_bootstrap4():
    form = SampleFormWithMedia()
    form.helper = FormHelper()
    form.helper.template_pack = 'bootstrap4'
    html = render_crispy_form(form)
    assert 'test.css' in html
    assert 'test.js' in html


def test_media_removed_when_include_media_is_false_with_uniform():
    form = SampleFormWithMedia()
    form.helper = FormHelper()
    form.helper.template_pack = 'uni_form'
    form.helper.include_media = False
    html = render_crispy_form(form)
    assert 'test.css' not in html
    assert 'test.js' not in html


def test_media_removed_when_include_media_is_false_with_bootstrap():
    form = SampleFormWithMedia()
    form.helper = FormHelper()
    form.helper.template_pack = 'bootstrap'
    form.helper.include_media = False
    html = render_crispy_form(form)
    assert 'test.css' not in html
    assert 'test.js' not in html


def test_media_removed_when_include_media_is_false_with_bootstrap3():
    form = SampleFormWithMedia()
    form.helper = FormHelper()
    form.helper.template_pack = 'bootstrap3'
    form.helper.include_media = False
    html = render_crispy_form(form)
    assert 'test.css' not in html
    assert 'test.js' not in html


def test_media_removed_when_include_media_is_false_with_bootstrap4():
    form = SampleFormWithMedia()
    form.helper = FormHelper()
    form.helper.template_pack = 'bootstrap4'
    form.helper.include_media = False
    html = render_crispy_form(form)
    assert 'test.css' not in html
    assert 'test.js' not in html


def test_attrs():
    form = SampleForm()
    form.helper = FormHelper()
    form.helper.attrs = {'id': 'TestIdForm', 'autocomplete': "off"}
    html = render_crispy_form(form)

    assert 'autocomplete="off"' in html
    assert 'id="TestIdForm"' in html


def test_template_context():
    helper = FormHelper()
    helper.attrs = {
        'id': 'test-form',
        'class': 'test-forms',
        'action': 'submit/test/form',
        'autocomplete': 'off',
    }
    node = CrispyFormNode('form', 'helper')
    context = node.get_response_dict(helper, {}, False)

    assert context['form_id'] == "test-form"
    assert context['form_attrs']['id'] == "test-form"
    assert "test-forms" in context['form_class']
    assert "test-forms" in context['form_attrs']['class']
    assert context['form_action'] == "submit/test/form"
    assert context['form_attrs']['action'] == "submit/test/form"
    assert context['form_attrs']['autocomplete'] == "off"


def test_template_context_using_form_attrs():
    helper = FormHelper()
    helper.form_id = 'test-form'
    helper.form_class = 'test-forms'
    helper.form_action = 'submit/test/form'
    node = CrispyFormNode('form', 'helper')
    context = node.get_response_dict(helper, {}, False)

    assert context['form_id'] == "test-form"
    assert context['form_attrs']['id'] == "test-form"
    assert "test-forms" in context['form_class']
    assert "test-forms" in context['form_attrs']['class']
    assert context['form_action'] == "submit/test/form"
    assert context['form_attrs']['action'] == "submit/test/form"


def test_template_helper_access():
    helper = FormHelper()
    helper.form_id = 'test-form'

    assert helper['form_id'] == 'test-form'


def test_without_helper(settings):
    template = Template("""
        {% load crispy_forms_tags %}
        {% crispy form %}
    """)
    c = Context({'form': SampleForm()})
    html = template.render(c)

    # Lets make sure everything loads right
    assert '<form' in html
    assert 'method="post"' in html
    assert 'action' not in html
    if settings.CRISPY_TEMPLATE_PACK == 'uni_form':
        assert 'uniForm' in html


def test_template_pack_override_compact(settings):
    current_pack = settings.CRISPY_TEMPLATE_PACK
    override_pack = current_pack == 'uni_form' and 'bootstrap' or 'uni_form'

    # {% crispy form 'template_pack_name' %}
    template = Template("""
        {%% load crispy_forms_tags %%}
        {%% crispy form "%s" %%}
    """ % override_pack)
    c = Context({'form': SampleForm()})
    html = template.render(c)

    if current_pack == 'uni_form':
        assert 'control-group' in html
    else:
        assert 'uniForm' in html


def test_template_pack_override_verbose(settings):
    current_pack = settings.CRISPY_TEMPLATE_PACK
    override_pack = current_pack == 'uni_form' and 'bootstrap' or 'uni_form'

    # {% crispy form helper 'template_pack_name' %}
    template = Template("""
        {%% load crispy_forms_tags %%}
        {%% crispy form form_helper "%s" %%}
    """ % override_pack)
    c = Context({'form': SampleForm(), 'form_helper': FormHelper()})
    html = template.render(c)

    if current_pack == 'uni_form':
        assert 'control-group' in html
    else:
        assert 'uniForm' in html


def test_template_pack_override_wrong():
    with pytest.raises(TemplateSyntaxError):
        Template("""
            {% load crispy_forms_tags %}
            {% crispy form 'foo' %}
        """)


def test_invalid_helper(settings):
    template = Template("""
        {% load crispy_forms_tags %}
        {% crispy form form_helper %}
    """)
    c = Context({'form': SampleForm(), 'form_helper': "invalid"})

    settings.CRISPY_FAIL_SILENTLY = settings.TEMPLATE_DEBUG = False
    with pytest.raises(TypeError):
        template.render(c)


def test_formset_with_helper_without_layout(settings):
    template = Template("""
        {% load crispy_forms_tags %}
        {% crispy testFormSet formset_helper %}
    """)

    form_helper = FormHelper()
    form_helper.form_id = 'thisFormsetRocks'
    form_helper.form_class = 'formsets-that-rock'
    form_helper.form_method = 'POST'
    form_helper.form_action = 'simpleAction'

    SampleFormSet = formset_factory(SampleForm, extra=3)
    testFormSet = SampleFormSet()

    c = Context({'testFormSet': testFormSet, 'formset_helper': form_helper, 'csrf_token': _get_new_csrf_key()})
    html = template.render(c)

    assert html.count('<form') == 1
    assert html.count("<input type='hidden' name='csrfmiddlewaretoken'") == 1

    # Check formset management form
    assert 'form-TOTAL_FORMS' in html
    assert 'form-INITIAL_FORMS' in html
    assert 'form-MAX_NUM_FORMS' in html

    assert 'formsets-that-rock' in html
    assert 'method="post"' in html
    assert 'id="thisFormsetRocks"' in html
    assert 'action="%s"' % reverse('simpleAction') in html
    if settings.CRISPY_TEMPLATE_PACK == 'uni_form':
        assert 'class="uniForm' in html


def test_CSRF_token_POST_form():
    form_helper = FormHelper()
    template = Template("""
        {% load crispy_forms_tags %}
        {% crispy form form_helper %}
    """)

    # The middleware only initializes the CSRF token when processing a real request
    # So using RequestContext or csrf(request) here does not work.
    # Instead I set the key `csrf_token` to a CSRF token manually, which `csrf_token` tag uses
    c = Context({'form': SampleForm(), 'form_helper': form_helper, 'csrf_token': _get_new_csrf_key()})
    html = template.render(c)

    assert "<input type='hidden' name='csrfmiddlewaretoken'" in html


def test_CSRF_token_GET_form():
    form_helper = FormHelper()
    form_helper.form_method = 'GET'
    template = Template("""
        {% load crispy_forms_tags %}
        {% crispy form form_helper %}
    """)

    c = Context({'form': SampleForm(), 'form_helper': form_helper, 'csrf_token': _get_new_csrf_key()})
    html = template.render(c)

    assert "<input type='hidden' name='csrfmiddlewaretoken'" not in html


def test_disable_csrf():
    form = SampleForm()
    helper = FormHelper()
    helper.disable_csrf = True
    html = render_crispy_form(form, helper, {'csrf_token': _get_new_csrf_key()})
    assert 'csrf' not in html


def test_render_hidden_fields():
    from .utils import contains_partial
    test_form = SampleForm()
    test_form.helper = FormHelper()
    test_form.helper.layout = Layout(
        'email'
    )
    test_form.helper.render_hidden_fields = True

    html = render_crispy_form(test_form)
    assert html.count('<input') == 1

    # Now hide a couple of fields
    for field in ('password1', 'password2'):
        test_form.fields[field].widget = forms.HiddenInput()

    html = render_crispy_form(test_form)
    assert html.count('<input') == 3
    assert html.count('hidden') == 2

    assert contains_partial(html, '<input name="password1" type="hidden"/>')
    assert contains_partial(html, '<input name="password2" type="hidden"/>')


def test_render_required_fields():
    test_form = SampleForm()
    test_form.helper = FormHelper()
    test_form.helper.layout = Layout(
        'email'
    )
    test_form.helper.render_required_fields = True

    html = render_crispy_form(test_form)
    assert html.count('<input') == 7


def test_helper_custom_template():
    form = SampleForm()
    form.helper = FormHelper()
    form.helper.template = 'custom_form_template.html'

    html = render_crispy_form(form)
    assert "<h1>Special custom form</h1>" in html


def test_helper_custom_field_template():
    form = SampleForm()
    form.helper = FormHelper()
    form.helper.layout = Layout(
        'password1',
        'password2',
    )
    form.helper.field_template = 'custom_field_template.html'

    html = render_crispy_form(form)
    assert html.count("<h1>Special custom field</h1>") == 2


@only_uni_form
def test_form_show_errors():
    form = SampleForm({
        'email': 'invalidemail',
        'first_name': 'first_name_too_long',
        'last_name': 'last_name_too_long',
        'password1': 'yes',
        'password2': 'yes',
        })
    form.helper = FormHelper()
    form.helper.layout = Layout(
        Field('email'),
        Field('first_name'),
        Field('last_name'),
        Field('password1'),
        Field('password2'),
    )
    form.is_valid()

    form.helper.form_show_errors = True
    html = render_crispy_form(form)
    assert html.count('error') == 9

    form.helper.form_show_errors = False
    html = render_crispy_form(form)
    assert html.count('error') == 0


@only_uni_form
def test_multifield_errors():
    form = SampleForm({
        'email': 'invalidemail',
        'password1': 'yes',
        'password2': 'yes',
    })
    form.helper = FormHelper()
    form.helper.layout = Layout(
        MultiField('legend', 'email')
    )
    form.is_valid()

    form.helper.form_show_errors = True
    html = render_crispy_form(form)
    assert html.count('error') == 3

    # Reset layout for avoiding side effects
    form.helper.layout = Layout(
        MultiField('legend', 'email')
    )
    form.helper.form_show_errors = False
    html = render_crispy_form(form)
    assert html.count('error') == 0


@only_bootstrap3
def test_bootstrap_form_show_errors():
    form = SampleForm({
        'email': 'invalidemail',
        'first_name': 'first_name_too_long',
        'last_name': 'last_name_too_long',
        'password1': 'yes',
        'password2': 'yes',
    })
    form.helper = FormHelper()
    form.helper.layout = Layout(
        AppendedText('email', 'whatever'),
        PrependedText('first_name', 'blabla'),
        PrependedAppendedText('last_name', 'foo', 'bar'),
        AppendedText('password1', 'whatever'),
        PrependedText('password2', 'blabla'),
    )
    form.is_valid()

    form.helper.form_show_errors = True
    html = render_crispy_form(form)
    assert html.count('error') == 6

    form.helper.form_show_errors = False
    html = render_crispy_form(form)
    assert html.count('error') == 0


@only_bootstrap4
def test_bootstrap_form_show_errors():
    form = SampleForm({
        'email': 'invalidemail',
        'first_name': 'first_name_too_long',
        'last_name': 'last_name_too_long',
        'password1': 'yes',
        'password2': 'yes',
    })
    form.helper = FormHelper()
    form.helper.layout = Layout(
        AppendedText('email', 'whatever'),
        PrependedText('first_name', 'blabla'),
        PrependedAppendedText('last_name', 'foo', 'bar'),
        AppendedText('password1', 'whatever'),
        PrependedText('password2', 'blabla'),
    )
    form.is_valid()

    form.helper.form_show_errors = True
    html = render_crispy_form(form)
    assert html.count('error') == 3

    form.helper.form_show_errors = False
    html = render_crispy_form(form)
    assert html.count('error') == 0


@only_bootstrap
def test_error_text_inline(settings):
    form = SampleForm({'email': 'invalidemail'})
    form.helper = FormHelper()
    layout = Layout(
        AppendedText('first_name', 'wat'),
        PrependedText('email', '@'),
        PrependedAppendedText('last_name', '@', 'wat'),
    )
    form.helper.layout = layout
    form.is_valid()
    html = render_crispy_form(form)

    help_class = 'help-inline'
    if settings.CRISPY_TEMPLATE_PACK == 'bootstrap3':
        help_class = 'help-block'
    elif settings.CRISPY_TEMPLATE_PACK == 'bootstrap4':
        help_class = 'invalid-feedback'

    matches = re.findall(
        '<span id="error_\d_\w*" class="%s"' % help_class, html, re.MULTILINE
    )
    assert len(matches) == 3

    form = SampleForm({'email': 'invalidemail'})
    form.helper = FormHelper()
    form.helper.layout = layout
    form.helper.error_text_inline = False
    html = render_crispy_form(form)

    if settings.CRISPY_TEMPLATE_PACK in ['bootstrap', 'bootstrap3']:
        help_class = 'help-block'
    elif settings.CRISPY_TEMPLATE_PACK == 'bootstrap4':
        help_class = 'invalid-feedback'

    matches = re.findall(
        '<p id="error_\d_\w*" class="%s"' % help_class,
        html,
        re.MULTILINE
    )
    assert len(matches) == 3


@only_bootstrap3
def test_error_and_help_inline():
    form = SampleForm({'email': 'invalidemail'})
    form.helper = FormHelper()
    form.helper.error_text_inline = False
    form.helper.help_text_inline = True
    form.helper.layout = Layout('email')
    form.is_valid()
    html = render_crispy_form(form)

    # Check that help goes before error, otherwise CSS won't work
    help_position = html.find('<span id="hint_id_email" class="help-inline">')
    error_position = html.find('<p id="error_1_id_email" class="help-block">')
    assert help_position < error_position

    # Viceversa
    form = SampleForm({'email': 'invalidemail'})
    form.helper = FormHelper()
    form.helper.error_text_inline = True
    form.helper.help_text_inline = False
    form.helper.layout = Layout('email')
    form.is_valid()
    html = render_crispy_form(form)

    # Check that error goes before help, otherwise CSS won't work
    error_position = html.find('<span id="error_1_id_email" class="help-inline">')
    help_position = html.find('<p id="hint_id_email" class="help-block">')
    assert error_position < help_position


@only_bootstrap4
def test_error_and_help_inline():
    form = SampleForm({'email': 'invalidemail'})
    form.helper = FormHelper()
    form.helper.error_text_inline = False
    form.helper.help_text_inline = True
    form.helper.layout = Layout('email')
    form.is_valid()
    html = render_crispy_form(form)

    # Check that help goes before error, otherwise CSS won't work
    help_position = html.find('<span id="hint_id_email" class="help-inline">')
    error_position = html.find('<p id="error_1_id_email" class="invalid-feedback">')
    assert help_position < error_position

    # Viceversa
    form = SampleForm({'email': 'invalidemail'})
    form.helper = FormHelper()
    form.helper.error_text_inline = True
    form.helper.help_text_inline = False
    form.helper.layout = Layout('email')
    form.is_valid()
    html = render_crispy_form(form)

    # Check that error goes before help, otherwise CSS won't work
    error_position = html.find('<span id="error_1_id_email" class="help-inline">')
    help_position = html.find('<small id="hint_id_email" class="text-muted">')
    assert error_position < help_position


@only_bootstrap
def test_form_show_labels():
    form = SampleForm()
    form.helper = FormHelper()
    form.helper.layout = Layout(
        'password1',
        FieldWithButtons(
            'password2',
            StrictButton("Confirm")
        ),
        PrependedText(
            'first_name',
            'Mr.'
        ),
        AppendedText(
            'last_name',
            '@'
        ),
        PrependedAppendedText(
            'datetime_field',
            'on',
            'secs'
        )
    )
    form.helper.form_show_labels = False

    html = render_crispy_form(form)
    assert html.count("<label") == 0


@only_bootstrap3
def test_label_class_and_field_class():
    form = SampleForm()
    form.helper = FormHelper()
    form.helper.label_class = 'col-lg-2'
    form.helper.field_class = 'col-lg-8'
    html = render_crispy_form(form)
    dom = parse_html(html)

    snippet = parse_html('<div class="form-group"> <div class="controls col-lg-offset-2 col-lg-8"> <div id="div_id_is_company" class="checkbox"> <label for="id_is_company" class=""> <input class="checkboxinput" id="id_is_company" name="is_company" type="checkbox" />company')
    assert dom.count(snippet)
    assert html.count('col-lg-8') == 7

    form.helper.label_class = 'col-sm-3 col-md-4'
    form.helper.field_class = 'col-sm-8 col-md-6'
    html = render_crispy_form(form)
    dom = parse_html(html)

    snippet = parse_html('<div class="form-group"> <div class="controls col-sm-offset-3 col-md-offset-4 col-sm-8 col-md-6"> <div id="div_id_is_company" class="checkbox"> <label for="id_is_company" class=""> <input class="checkboxinput" id="id_is_company" name="is_company" type="checkbox" />company' )
    assert dom.count(snippet)
    assert html.count('col-sm-8') == 7


@only_bootstrap3
def test_template_pack():
    form = SampleForm()
    form.helper = FormHelper()
    form.helper.template_pack = 'uni_form'
    html = render_crispy_form(form)
    assert 'form-control' not in html
    assert 'ctrlHolder' in html


@only_bootstrap4
def test_label_class_and_field_class_bs4():
    form = SampleForm()
    form.helper = FormHelper()
    form.helper.label_class = 'col-lg-2'
    form.helper.field_class = 'col-lg-8'
    html = render_crispy_form(form)

    assert '<div class="form-group">' in html
    assert '<div class="col-lg-offset-2 col-lg-8">' in html
    assert html.count('col-lg-8') == 7

    form.helper.label_class = 'col-sm-3 col-md-4'
    form.helper.field_class = 'col-sm-8 col-md-6'
    html = render_crispy_form(form)

    assert '<div class="form-group">' in html
    assert '<div class="col-sm-offset-3 col-md-offset-4 col-sm-8 col-md-6">' in html
    assert html.count('col-sm-8') == 7


@only_bootstrap4
def test_template_pack_bs4():
    form = SampleForm()
    form.helper = FormHelper()
    form.helper.template_pack = 'uni_form'
    html = render_crispy_form(form)
    assert 'form-control' not in html
    assert 'ctrlHolder' in html


def test_passthrough_context():
    """
    Test to ensure that context is passed through implicitly from outside of
    the crispy form into the crispy form templates.
    """
    form = SampleForm()
    form.helper = FormHelper()
    form.helper.template = 'custom_form_template_with_context.html'

    c = {
        'prefix': 'foo',
        'suffix': 'bar'
    }

    html = render_crispy_form(form, helper=form.helper, context=c)
    assert "Got prefix: foo" in html
    assert "Got suffix: bar" in html





@only_bootstrap3
def test_bootstrap3_does_add_form_control_class_to_non_multivaluefield():
    form = SampleForm()
    form.helper = FormHelper()
    form.helper.template_pack = 'bootstrap3'
    html = render_crispy_form(form)
    assert 'form-control' in html


@only_bootstrap3
def test_bootstrap3_does_not_add_form_control_class_to_multivaluefield():
    form = SampleFormWithMultiValueField()
    form.helper = FormHelper()
    form.helper.template_pack = 'bootstrap3'
    html = render_crispy_form(form)
    assert 'form-control' not in html
