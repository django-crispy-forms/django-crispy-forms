# -*- coding: utf-8 -*-
import os.path
import re

import django
from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse
from django.forms.forms import BoundField
from django.forms.models import formset_factory, modelformset_factory
from django.template import Context, TemplateSyntaxError, RequestContext
from django.template import loader
from django.middleware.csrf import _get_new_csrf_key
from django.shortcuts import render_to_response
from django.test import TestCase, RequestFactory
from django.utils.translation import ugettext_lazy as _

from crispy_forms.compatibility import string_types, text_type
from crispy_forms.exceptions import DynamicError
from crispy_forms.helper import FormHelper, FormHelpersException
from crispy_forms.layout import Submit, Reset, Hidden, Button
from crispy_forms.layout import (
    Layout, Fieldset, MultiField, Row, Column, HTML, ButtonHolder,
    Div, Field, MultiWidgetField
)
from crispy_forms.bootstrap import (
    AppendedPrependedText, AppendedText, PrependedText, InlineCheckboxes,
    FieldWithButtons, StrictButton, InlineRadios, Tab, TabHolder,
    AccordionGroup, Accordion
)
from crispy_forms.utils import render_crispy_form
from crispy_forms.templatetags.crispy_forms_tags import CrispyFormNode
from crispy_forms.templatetags.crispy_forms_field import crispy_addon

from crispy_forms.tests.forms import (
    TestForm, TestForm2, TestForm3, ExampleForm, CheckboxesTestForm,
    FormWithMeta, TestForm4, CrispyTestModel, TestForm5
)
from crispy_forms.tests.utils import override_settings


class CrispyTestCase(TestCase):
    def setUp(self):
        template_dirs = [os.path.join(os.path.dirname(__file__), 'templates')]
        template_dirs = template_dirs + list(settings.TEMPLATE_DIRS)
        template_loaders = ['django.template.loaders.filesystem.Loader']
        template_loaders = template_loaders + list(settings.TEMPLATE_LOADERS)

        # ensuring test templates directory is loaded first
        self.__overriden_settings = override_settings(**{
            'TEMPLATE_LOADERS': template_loaders,
            'TEMPLATE_DIRS': template_dirs,
        })
        self.__overriden_settings.enable()

        # resetting template loaders cache
        self.__template_source_loaders = loader.template_source_loaders
        loader.template_source_loaders = None

    def tearDown(self):
        loader.template_source_loaders = self.__template_source_loaders
        self.__overriden_settings.disable()

    @property
    def current_template_pack(self):
        return getattr(settings, 'CRISPY_TEMPLATE_PACK', 'bootstrap')


class TestBasicFunctionalityTags(CrispyTestCase):
    def test_as_crispy_errors_form_without_non_field_errors(self):
        template = loader.get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {{ form|as_crispy_errors }}
        """)
        form = TestForm({'password1': "god", 'password2': "god"})
        form.is_valid()

        c = Context({'form': form})
        html = template.render(c)
        self.assertFalse("errorMsg" in html or "alert" in html)

    def test_as_crispy_errors_form_with_non_field_errors(self):
        template = loader.get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {{ form|as_crispy_errors }}
        """)
        form = TestForm({'password1': "god", 'password2': "wargame"})
        form.is_valid()

        c = Context({'form': form})
        html = template.render(c)
        self.assertTrue("errorMsg" in html or "alert" in html)
        self.assertTrue("<li>Passwords dont match</li>" in html)
        self.assertFalse("<h3>" in html)

    def test_crispy_filter_with_form(self):
        template = loader.get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {{ form|crispy }}
        """)
        c = Context({'form': TestForm()})
        html = template.render(c)

        self.assertTrue("<td>" not in html)
        self.assertTrue("id_is_company" in html)
        self.assertEqual(html.count('<label'), 7)

    def test_crispy_filter_with_formset(self):
        template = loader.get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {{ testFormset|crispy }}
        """)

        TestFormset = formset_factory(TestForm, extra = 4)
        testFormset = TestFormset()

        c = Context({'testFormset': testFormset})
        html = template.render(c)

        self.assertEqual(html.count('<form'), 0)
        # Check formset management form
        self.assertTrue('form-TOTAL_FORMS' in html)
        self.assertTrue('form-INITIAL_FORMS' in html)
        self.assertTrue('form-MAX_NUM_FORMS' in html)

    def test_classes_filter(self):
        template = loader.get_template_from_string(u"""
            {% load crispy_forms_field %}
            {{ testField|classes }}
        """)

        test_form = TestForm()
        test_form.fields['email'].widget.attrs.update({'class': 'email-fields'})
        c = Context({'testField': test_form.fields['email']})
        html = template.render(c)
        self.assertTrue('email-fields' in html)

    def test_crispy_field_and_class_converters(self):
        if hasattr(settings, 'CRISPY_CLASS_CONVERTERS'):
            template = loader.get_template_from_string(u"""
                {% load crispy_forms_field %}
                {% crispy_field testField 'class' 'error' %}
            """)
            test_form = TestForm()
            field_instance = test_form.fields['email']
            bound_field = BoundField(test_form, field_instance, 'email')

            c = Context({'testField': bound_field})
            html = template.render(c)
            self.assertTrue('error' in html)
            self.assertTrue('inputtext' in html)

    def test_crispy_addon(self):
        test_form = TestForm()
        field_instance = test_form.fields['email']
        bound_field = BoundField(test_form, field_instance, 'email')
        # prepend tests
        self.assertIn("input-prepend", crispy_addon(bound_field, prepend="Work"))
        self.assertNotIn("input-append", crispy_addon(bound_field, prepend="Work"))
        # append tests
        self.assertNotIn("input-prepend", crispy_addon(bound_field, append="Primary"))
        self.assertIn("input-append", crispy_addon(bound_field, append="Secondary"))
        # prepend and append tests
        self.assertIn("input-append", crispy_addon(bound_field, prepend="Work", append="Primary"))
        self.assertIn("input-prepend", crispy_addon(bound_field, prepend="Work", append="Secondary"))
        # errors
        with self.assertRaises(TypeError):
            crispy_addon()
            crispy_addon(bound_field)

class TestFormHelpers(CrispyTestCase):
    urls = 'crispy_forms.tests.urls'

    def test_inputs(self):
        form_helper = FormHelper()
        form_helper.add_input(Submit('my-submit', 'Submit', css_class="button white"))
        form_helper.add_input(Reset('my-reset', 'Reset'))
        form_helper.add_input(Hidden('my-hidden', 'Hidden'))
        form_helper.add_input(Button('my-button', 'Button'))

        template = loader.get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {% crispy form form_helper %}
        """)
        c = Context({'form': TestForm(), 'form_helper': form_helper})
        html = template.render(c)

        self.assertTrue('button white' in html)
        self.assertTrue('id="submit-id-my-submit"' in html)
        self.assertTrue('id="reset-id-my-reset"' in html)
        self.assertTrue('name="my-hidden"' in html)
        self.assertTrue('id="button-id-my-button"' in html)

        if self.current_template_pack == 'uni_form':
            self.assertTrue('submit submitButton' in html)
            self.assertTrue('reset resetButton' in html)
            self.assertTrue('class="button"' in html)
        else:
            self.assertTrue('class="btn"' in html)
            self.assertTrue('btn btn-primary' in html)
            self.assertTrue('btn btn-inverse' in html)
            self.assertEqual(len(re.findall(r'<input[^>]+> <', html)), 8)

    def test_invalid_form_method(self):
        form_helper = FormHelper()
        try:
            form_helper.form_method = "superPost"
            self.fail("Setting an invalid form_method within the helper should raise an Exception")
        except FormHelpersException:
            pass

    def test_form_with_helper_without_layout(self):
        form_helper = FormHelper()
        form_helper.form_id = 'this-form-rocks'
        form_helper.form_class = 'forms-that-rock'
        form_helper.form_method = 'GET'
        form_helper.form_action = 'simpleAction'
        form_helper.form_error_title = 'ERRORS'

        template = loader.get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {% crispy testForm form_helper %}
        """)

        # now we render it, with errors
        form = TestForm({'password1': 'wargame','password2': 'god'})
        form.is_valid()
        c = Context({'testForm': form, 'form_helper': form_helper})
        html = template.render(c)

        # Lets make sure everything loads right
        self.assertTrue(html.count('<form'), 1)
        self.assertTrue('forms-that-rock' in html)
        self.assertTrue('method="get"' in html)
        self.assertTrue('id="this-form-rocks"' in html)
        self.assertTrue('action="%s"' % reverse('simpleAction') in html)

        if (self.current_template_pack == 'uni_form'):
            self.assertTrue('class="uniForm' in html)

        self.assertTrue("ERRORS" in html)
        self.assertTrue("<li>Passwords dont match</li>" in html)

        # now lets remove the form tag and render it again. All the True items above
        # should now be false because the form tag is removed.
        form_helper.form_tag = False
        html = template.render(c)
        self.assertFalse('<form' in html)
        self.assertFalse('forms-that-rock' in html)
        self.assertFalse('method="get"' in html)
        self.assertFalse('id="this-form-rocks"' in html)

    def test_form_show_errors_non_field_errors(self):
        form = TestForm({'password1': 'wargame', 'password2': 'god'})
        form.helper = FormHelper()
        form.helper.form_show_errors = True
        form.is_valid()

        template = loader.get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {% crispy testForm %}
        """)

        # First we render with errors
        c = Context({'testForm': form})
        html = template.render(c)

        # Ensure those errors were rendered
        self.assertTrue('<li>Passwords dont match</li>' in html)
        self.assertTrue(text_type(_('This field is required.')) in html)
        self.assertTrue('error' in html)

        # Now we render without errors
        form.helper.form_show_errors = False
        c = Context({'testForm': form})
        html = template.render(c)

        # Ensure errors were not rendered
        self.assertFalse('<li>Passwords dont match</li>' in html)
        self.assertFalse(text_type(_('This field is required.')) in html)
        self.assertFalse('error' in html)

    def test_form_show_errors(self):
        form = TestForm({
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
            AppendedPrependedText('last_name', 'foo', 'bar'),
            MultiField('legend', 'password1', 'password2')
        )
        form.is_valid()

        form.helper.form_show_errors = True
        html = render_crispy_form(form)
        self.assertEqual(html.count('error'), 6)

        form.helper.form_show_errors = False
        html = render_crispy_form(form)
        self.assertEqual(html.count('error'), 0)

    def test_multifield_errors(self):
        form = TestForm({
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
        self.assertEqual(html.count('error'), 3)

        # Reset layout for avoiding side effects
        form.helper.layout = Layout(
            MultiField('legend', 'email')
        )
        form.helper.form_show_errors = False
        html = render_crispy_form(form)
        self.assertEqual(html.count('error'), 0)

    def test_html5_required(self):
        form = TestForm()
        form.helper = FormHelper()
        form.helper.html5_required = True
        html = render_crispy_form(form)
        # 6 out of 7 fields are required and an extra one for the SplitDateTimeWidget makes 7.
        self.assertEqual(html.count('required="required"'), 7)

        form = TestForm()
        form.helper = FormHelper()
        form.helper.html5_required = False
        html = render_crispy_form(form)

    def test_error_text_inline(self):
        form = TestForm({'email': 'invalidemail'})
        form.helper = FormHelper()
        layout = Layout(
            AppendedText('first_name', 'wat'),
            PrependedText('email', '@'),
            AppendedPrependedText('last_name', '@', 'wat'),
        )
        form.helper.layout = layout
        form.is_valid()
        html = render_crispy_form(form)

        matches = re.findall('<span id="error_\d_\w*" class="help-inline"', html, re.MULTILINE)
        self.assertEqual(len(matches), 3)

        form = TestForm({'email': 'invalidemail'})
        form.helper = FormHelper()
        form.helper.layout = layout
        form.helper.error_text_inline = False
        html = render_crispy_form(form)

        matches = re.findall('<p id="error_\d_\w*" class="help-block"', html, re.MULTILINE)
        self.assertEqual(len(matches), 3)

    def test_error_and_help_inline(self):
        form = TestForm({'email': 'invalidemail'})
        form.helper = FormHelper()
        form.helper.error_text_inline = False
        form.helper.help_text_inline = True
        form.helper.layout = Layout('email')
        form.is_valid()
        html = render_crispy_form(form)

        # Check that help goes before error, otherwise CSS won't work
        if self.current_template_pack == 'bootstrap':
            help_position = html.find('<span id="hint_id_email" class="help-inline">')
            error_position = html.find('<p id="error_1_id_email" class="help-block">')
            self.assertTrue(help_position < error_position)

        # Viceversa
        form = TestForm({'email': 'invalidemail'})
        form.helper = FormHelper()
        form.helper.error_text_inline = True
        form.helper.help_text_inline = False
        form.helper.layout = Layout('email')
        form.is_valid()
        html = render_crispy_form(form)

        # Check that error goes before help, otherwise CSS won't work
        if self.current_template_pack == 'bootstrap':
            error_position = html.find('<span id="error_1_id_email" class="help-inline">')
            help_position = html.find('<p id="hint_id_email" class="help-block">')
            self.assertTrue(error_position < help_position)

    def test_attrs(self):
        form = TestForm()
        form.helper = FormHelper()
        form.helper.attrs = {'id': 'TestIdForm', 'autocomplete': "off"}
        html = render_crispy_form(form)

        self.assertTrue('autocomplete="off"' in html)
        self.assertTrue('id="TestIdForm"' in html)

    def test_template_context(self):
        helper = FormHelper()
        helper.attrs = {
            'id': 'test-form',
            'class': 'test-forms',
            'action': 'submit/test/form',
            'autocomplete': 'off',
        }
        node = CrispyFormNode('form', 'helper')
        context = node.get_response_dict(helper, {}, False)

        self.assertEqual(context['form_id'], "test-form")
        self.assertEqual(context['form_attrs']['id'], "test-form")
        self.assertTrue("test-forms" in context['form_class'])
        self.assertTrue("test-forms" in context['form_attrs']['class'])
        self.assertEqual(context['form_action'], "submit/test/form")
        self.assertEqual(context['form_attrs']['action'], "submit/test/form")
        self.assertEqual(context['form_attrs']['autocomplete'], "off")

    def test_template_context_using_form_attrs(self):
        helper = FormHelper()
        helper.form_id = 'test-form'
        helper.form_class = 'test-forms'
        helper.form_action = 'submit/test/form'
        node = CrispyFormNode('form', 'helper')
        context = node.get_response_dict(helper, {}, False)

        self.assertEqual(context['form_id'], "test-form")
        self.assertEqual(context['form_attrs']['id'], "test-form")
        self.assertTrue("test-forms" in context['form_class'])
        self.assertTrue("test-forms" in context['form_attrs']['class'])
        self.assertEqual(context['form_action'], "submit/test/form")
        self.assertEqual(context['form_attrs']['action'], "submit/test/form")

    def test_template_helper_access(self):
        helper = FormHelper()
        helper.form_id = 'test-form'

        self.assertEqual(helper['form_id'], 'test-form')

    def test_without_helper(self):
        template = loader.get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {% crispy form %}
        """)
        c = Context({'form': TestForm()})
        html = template.render(c)

        # Lets make sure everything loads right
        self.assertTrue('<form' in html)
        self.assertTrue('method="post"' in html)
        self.assertFalse('action' in html)
        if (self.current_template_pack == 'uni_form'):
            self.assertTrue('uniForm' in html)

    def test_template_pack_override(self):
        current_pack = self.current_template_pack
        override_pack = current_pack == 'uni_form' and 'bootstrap' or 'uni_form'

        # Syntax {% crispy form 'template_pack_name' %}
        template = loader.get_template_from_string(u"""
            {%% load crispy_forms_tags %%}
            {%% crispy form "%s" %%}
        """ % override_pack)
        c = Context({'form': TestForm()})
        html = template.render(c)

        # Syntax {% crispy form helper 'template_pack_name' %}
        template = loader.get_template_from_string(u"""
            {%% load crispy_forms_tags %%}
            {%% crispy form form_helper "%s" %%}
        """ % override_pack)
        c = Context({'form': TestForm(), 'form_helper': FormHelper()})
        html2 = template.render(c)

        if (current_pack == 'uni_form'):
            self.assertTrue('control-group' in html)
            self.assertTrue('control-group' in html2)
        else:
            self.assertTrue('uniForm' in html)
            self.assertTrue('uniForm' in html2)

    def test_invalid_helper(self):
        template = loader.get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {% crispy form form_helper %}
        """)
        c = Context({'form': TestForm(), 'form_helper': "invalid"})

        settings.CRISPY_FAIL_SILENTLY = False
        # Django >= 1.4 is not wrapping exceptions in TEMPLATE_DEBUG mode
        if settings.TEMPLATE_DEBUG and django.get_version() < '1.4':
            self.assertRaises(TemplateSyntaxError, lambda:template.render(c))
        else:
            self.assertRaises(TypeError, lambda:template.render(c))
        del settings.CRISPY_FAIL_SILENTLY

    def test_formset_with_helper_without_layout(self):
        template = loader.get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {% crispy testFormSet formset_helper %}
        """)

        form_helper = FormHelper()
        form_helper.form_id = 'thisFormsetRocks'
        form_helper.form_class = 'formsets-that-rock'
        form_helper.form_method = 'POST'
        form_helper.form_action = 'simpleAction'

        TestFormSet = formset_factory(TestForm, extra = 3)
        testFormSet = TestFormSet()

        c = Context({'testFormSet': testFormSet, 'formset_helper': form_helper, 'csrf_token': _get_new_csrf_key()})
        html = template.render(c)

        self.assertEqual(html.count('<form'), 1)
        self.assertEqual(html.count("<input type='hidden' name='csrfmiddlewaretoken'"), 1)

        # Check formset management form
        self.assertTrue('form-TOTAL_FORMS' in html)
        self.assertTrue('form-INITIAL_FORMS' in html)
        self.assertTrue('form-MAX_NUM_FORMS' in html)

        self.assertTrue('formsets-that-rock' in html)
        self.assertTrue('method="post"' in html)
        self.assertTrue('id="thisFormsetRocks"' in html)
        self.assertTrue('action="%s"' % reverse('simpleAction') in html)
        if (self.current_template_pack == 'uni_form'):
            self.assertTrue('class="uniForm' in html)

    def test_CSRF_token_POST_form(self):
        form_helper = FormHelper()
        template = loader.get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {% crispy form form_helper %}
        """)

        # The middleware only initializes the CSRF token when processing a real request
        # So using RequestContext or csrf(request) here does not work.
        # Instead I set the key `csrf_token` to a CSRF token manually, which `csrf_token` tag uses
        c = Context({'form': TestForm(), 'form_helper': form_helper, 'csrf_token': _get_new_csrf_key()})
        html = template.render(c)

        self.assertTrue("<input type='hidden' name='csrfmiddlewaretoken'" in html)

    def test_CSRF_token_GET_form(self):
        form_helper = FormHelper()
        form_helper.form_method = 'GET'
        template = loader.get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {% crispy form form_helper %}
        """)

        c = Context({'form': TestForm(), 'form_helper': form_helper, 'csrf_token': _get_new_csrf_key()})
        html = template.render(c)

        self.assertFalse("<input type='hidden' name='csrfmiddlewaretoken'" in html)

    def test_disable_csrf(self):
        form = TestForm()
        helper = FormHelper()
        helper.disable_csrf = True
        html = render_crispy_form(form, helper, {'csrf_token': _get_new_csrf_key()})
        self.assertFalse('csrf' in html)

    def test_render_hidden_fields(self):
        test_form = TestForm()
        test_form.helper = FormHelper()
        test_form.helper.layout = Layout(
            'email'
        )
        test_form.helper.render_hidden_fields = True

        html = render_crispy_form(test_form)
        self.assertEqual(html.count('<input'), 1)

        # Now hide a couple of fields
        for field in ('password1', 'password2'):
            test_form.fields[field].widget = forms.HiddenInput()

        html = render_crispy_form(test_form)
        self.assertEqual(html.count('<input'), 3)
        self.assertEqual(html.count('hidden'), 2)

        if django.get_version() < '1.5':
            self.assertEqual(html.count('type="hidden" name="password1"'), 1)
            self.assertEqual(html.count('type="hidden" name="password2"'), 1)
        else:
            self.assertEqual(html.count('name="password1" type="hidden"'), 1)
            self.assertEqual(html.count('name="password2" type="hidden"'), 1)

    def test_render_required_fields(self):
        test_form = TestForm()
        test_form.helper = FormHelper()
        test_form.helper.layout = Layout(
            'email'
        )
        test_form.helper.render_required_fields = True

        html = render_crispy_form(test_form)
        self.assertEqual(html.count('<input'), 7)

    def test_helper_custom_template(self):
        form = TestForm()
        form.helper = FormHelper()
        form.helper.template = 'custom_form_template.html'

        html = render_crispy_form(form)
        self.assertTrue("<h1>Special custom form</h1>" in html)

    def test_helper_custom_field_template(self):
        form = TestForm()
        form.helper = FormHelper()
        form.helper.layout = Layout(
            'password1',
            'password2',
        )
        form.helper.field_template = 'custom_field_template.html'

        html = render_crispy_form(form)
        self.assertEqual(html.count("<h1>Special custom field</h1>"), 2)

    def test_form_show_labels(self):
        form = TestForm()
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
            AppendedPrependedText(
                'datetime_field',
                'on',
                'secs'
            )
        )
        form.helper.form_show_labels = False

        if self.current_template_pack == 'bootstrap':
            html = render_crispy_form(form)
            self.assertEqual(html.count("<label"), 0)


class TestFormLayout(CrispyTestCase):
    urls = 'crispy_forms.tests.urls'

    def test_invalid_unicode_characters(self):
        # Adds a BooleanField that uses non valid unicode characters "ñ"
        form_helper = FormHelper()
        form_helper.add_layout(
            Layout(
                'españa'
            )
        )

        template = loader.get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {% crispy form form_helper %}
        """)
        c = Context({'form': TestForm(), 'form_helper': form_helper})
        settings.CRISPY_FAIL_SILENTLY = False
        self.assertRaises(Exception, lambda:template.render(c))
        del settings.CRISPY_FAIL_SILENTLY

    def test_meta_extra_fields_with_missing_fields(self):
        form = FormWithMeta()
        # We remove email field on the go
        del form.fields['email']

        form_helper = FormHelper()
        form_helper.layout = Layout(
            'first_name',
        )

        template = loader.get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {% crispy form form_helper %}
        """)
        c = Context({'form': form, 'form_helper': form_helper})
        html = template.render(c)
        self.assertFalse('email' in html)

    def test_layout_unresolved_field(self):
        form_helper = FormHelper()
        form_helper.add_layout(
            Layout(
                'typo'
            )
        )

        template = loader.get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {% crispy form form_helper %}
        """)
        c = Context({'form': TestForm(), 'form_helper': form_helper})
        settings.CRISPY_FAIL_SILENTLY = False
        self.assertRaises(Exception, lambda:template.render(c))
        del settings.CRISPY_FAIL_SILENTLY

    def test_double_rendered_field(self):
        form_helper = FormHelper()
        form_helper.add_layout(
            Layout(
                'is_company', 'is_company'
            )
        )

        template = loader.get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {% crispy form form_helper %}
        """)
        c = Context({'form': TestForm(), 'form_helper': form_helper})
        settings.CRISPY_FAIL_SILENTLY = False
        self.assertRaises(Exception, lambda:template.render(c))
        del settings.CRISPY_FAIL_SILENTLY

    def test_context_pollution(self):
        form = ExampleForm()
        form2 = TestForm()

        template = loader.get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {{ form.as_ul }}
            {% crispy form2 %}
            {{ form.as_ul }}
        """)
        c = Context({'form': form, 'form2': form2})
        html = template.render(c)

        self.assertEqual(html.count('name="comment"'), 2)
        self.assertEqual(html.count('name="is_company"'), 1)

    def test_hidden_fields(self):
        form = TestForm()
        # All fields hidden
        for field in form.fields:
            form.fields[field].widget = forms.HiddenInput()

        form.helper = FormHelper()
        form.helper.layout = Layout(
            AppendedText('password1', 'foo'),
            PrependedText('password2', 'bar'),
            AppendedPrependedText('email', 'bar'),
            InlineCheckboxes('first_name'),
            InlineRadios('last_name'),
        )
        html = render_crispy_form(form)
        self.assertEqual(html.count("<input"), 5)
        self.assertEqual(html.count('type="hidden"'), 5)
        self.assertEqual(html.count('<label'), 0)

    def test_field_with_buttons(self):
        form = TestForm()
        form.helper = FormHelper()
        form.helper.layout = Layout(
            FieldWithButtons(
                Field('password1', css_class="span4"),
                StrictButton("Go!", css_id="go-button"),
                StrictButton("No!", css_class="extra"),
                StrictButton("Test", type="submit", name="whatever", value="something"),
                css_class="extra",
                autocomplete="off"
            )
        )
        html = render_crispy_form(form)
        self.assertEqual(html.count('class="control-group extra"'), 1)
        self.assertEqual(html.count('autocomplete="off"'), 1)
        self.assertEqual(html.count('class="input-append"'), 1)
        self.assertEqual(html.count('class="span4'), 1)
        self.assertEqual(html.count('id="go-button"'), 1)
        self.assertEqual(html.count("Go!"), 1)
        self.assertEqual(html.count("No!"), 1)
        self.assertEqual(html.count('class="btn"'), 2)
        self.assertEqual(html.count('class="btn extra"'), 1)
        self.assertEqual(html.count('type="submit"'), 1)
        self.assertEqual(html.count('name="whatever"'), 1)
        self.assertEqual(html.count('value="something"'), 1)

        if self.current_template_pack == 'bootstrap':
            # Make sure white spaces between buttons are there in bootstrap
            self.assertEqual(len(re.findall(r'</button> <', html)), 3)

    def test_layout_fieldset_row_html_with_unicode_fieldnames(self):
        form_helper = FormHelper()
        form_helper.add_layout(
            Layout(
                Fieldset(
                    u'Company Data',
                    u'is_company',
                    css_id = "fieldset_company_data",
                    css_class = "fieldsets",
                    title = "fieldset_title",
                    test_fieldset = "123"
                ),
                Fieldset(
                    u'User Data',
                    u'email',
                    Row(
                        u'password1',
                        u'password2',
                        css_id = "row_passwords",
                        css_class = "rows",
                    ),
                    HTML('<a href="#" id="testLink">test link</a>'),
                    HTML(u"""
                        {% if flag %}{{ message }}{% endif %}
                    """),
                    u'first_name',
                    u'last_name',
                )
            )
        )

        template = loader.get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {% crispy form form_helper %}
        """)
        c = Context({
            'form': TestForm(),
            'form_helper': form_helper,
            'flag': True,
            'message': "Hello!",
        })
        html = template.render(c)

        self.assertTrue('id="fieldset_company_data"' in html)
        self.assertTrue('class="fieldsets' in html)
        self.assertTrue('title="fieldset_title"' in html)
        self.assertTrue('test-fieldset="123"' in html)
        self.assertTrue('id="row_passwords"' in html)
        self.assertEqual(html.count('<label'), 6)

        if self.current_template_pack == 'uni_form':
            self.assertTrue('class="formRow rows"' in html)
        else:
            self.assertTrue('class="row rows"' in html)
        self.assertTrue('Hello!' in html)
        self.assertTrue('testLink' in html)

    def test_second_layout_multifield_column_buttonholder_submit_div(self):
        form_helper = FormHelper()
        form_helper.add_layout(
            Layout(
                MultiField("Some company data",
                    'is_company',
                    'email',
                    css_id = "multifield_info",
                    title = "multifield_title",
                    multifield_test = "123"
                ),
                Column(
                    'first_name',
                    'last_name',
                    css_id = "column_name",
                    css_class = "columns",
                ),
                ButtonHolder(
                    Submit('Save the world', '{{ value_var }}', css_class='button white', data_id='test', data_name='test'),
                    Submit('store', 'Store results')
                ),
                Div(
                    'password1',
                    'password2',
                    css_id="custom-div",
                    css_class="customdivs",
                    test_markup="123"
                )
            )
        )

        template = loader.get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {% crispy form form_helper %}
        """)
        c = Context({'form': TestForm(), 'form_helper': form_helper, 'value_var': "Save"})
        html = template.render(c)

        self.assertTrue('multiField' in html)
        self.assertTrue('formColumn' in html)
        self.assertTrue('id="multifield_info"' in html)
        self.assertTrue('title="multifield_title"' in html)
        self.assertTrue('multifield-test="123"' in html)
        self.assertTrue('id="column_name"' in html)
        self.assertTrue('class="formColumn columns"' in html)
        self.assertTrue('class="buttonHolder">' in html)
        self.assertTrue('input type="submit"' in html)
        self.assertTrue('button white' in html)
        self.assertTrue('data-id="test"' in html)
        self.assertTrue('data-name="test"' in html)
        self.assertTrue('name="save-the-world"' in html)
        self.assertTrue('value="Save"' in html)
        self.assertTrue('name="store"' in html)
        self.assertTrue('value="Store results"' in html)
        self.assertTrue('id="custom-div"' in html)
        self.assertTrue('class="customdivs"' in html)
        self.assertTrue('test-markup="123"' in html)

    def test_layout_within_layout(self):
        form_helper = FormHelper()
        form_helper.add_layout(
            Layout(
                Layout(
                    MultiField("Some company data",
                        'is_company',
                        'email',
                        css_id = "multifield_info",
                    ),
                ),
                Column(
                    'first_name',
                    # 'last_name', Missing a field on purpose
                    css_id = "column_name",
                    css_class = "columns",
                ),
                ButtonHolder(
                    Submit('Save', 'Save', css_class='button white'),
                ),
                Div(
                    'password1',
                    'password2',
                    css_id="custom-div",
                    css_class="customdivs",
                )
            )
        )

        template = loader.get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {% crispy form form_helper %}
        """)
        c = Context({'form': TestForm(), 'form_helper': form_helper})
        html = template.render(c)

        self.assertTrue('multiField' in html)
        self.assertTrue('formColumn' in html)
        self.assertTrue('id="multifield_info"' in html)
        self.assertTrue('id="column_name"' in html)
        self.assertTrue('class="formColumn columns"' in html)
        self.assertTrue('class="buttonHolder">' in html)
        self.assertTrue('input type="submit"' in html)
        self.assertTrue('name="Save"' in html)
        self.assertTrue('id="custom-div"' in html)
        self.assertTrue('class="customdivs"' in html)
        self.assertFalse('last_name' in html)

    def test_change_layout_dynamically_delete_field(self):
        template = loader.get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {% crispy form form_helper %}
        """)

        form = TestForm()
        form_helper = FormHelper()
        form_helper.add_layout(
            Layout(
                Fieldset(
                    u'Company Data',
                    'is_company',
                    'email',
                    'password1',
                    'password2',
                    css_id = "multifield_info",
                ),
                Column(
                    'first_name',
                    'last_name',
                    css_id = "column_name",
                )
            )
        )

        # We remove email field on the go
        # Layout needs to be adapted for the new form fields
        del form.fields['email']
        del form_helper.layout.fields[0].fields[1]

        c = Context({'form': form, 'form_helper': form_helper})
        html = template.render(c)
        self.assertFalse('email' in html)

    def test_formset_layout(self):
        TestFormSet = formset_factory(TestForm, extra=3)
        formset = TestFormSet()
        helper = FormHelper()
        helper.form_id = 'thisFormsetRocks'
        helper.form_class = 'formsets-that-rock'
        helper.form_method = 'POST'
        helper.form_action = 'simpleAction'
        helper.layout = Layout(
            Fieldset("Item {{ forloop.counter }}",
                'is_company',
                'email',
            ),
            HTML("{% if forloop.first %}Note for first form only{% endif %}"),
            Row('password1', 'password2'),
            Fieldset("",
                'first_name',
                'last_name'
            )
        )

        html = render_crispy_form(
            form=formset, helper=helper, context={'csrf_token': _get_new_csrf_key()}
        )

        # Check formset fields
        django_version = django.get_version()
        if django_version < '1.5':
            self.assertEqual(html.count(
                'type="hidden" name="form-TOTAL_FORMS" value="3" id="id_form-TOTAL_FORMS"'
            ), 1)
            self.assertEqual(html.count(
                'type="hidden" name="form-INITIAL_FORMS" value="0" id="id_form-INITIAL_FORMS"'
            ), 1)
            if (django_version >= '1.4' and django_version < '1.4.4') or django_version < '1.3.6':
                self.assertEqual(html.count(
                    'type="hidden" name="form-MAX_NUM_FORMS" id="id_form-MAX_NUM_FORMS"'
                ), 1)
            else:
                self.assertEqual(html.count(
                    'type="hidden" name="form-MAX_NUM_FORMS" value="1000" id="id_form-MAX_NUM_FORMS"'
                ), 1)
        else:
            self.assertEqual(html.count(
                'id="id_form-TOTAL_FORMS" name="form-TOTAL_FORMS" type="hidden" value="3"'
            ), 1)
            self.assertEqual(html.count(
                'id="id_form-INITIAL_FORMS" name="form-INITIAL_FORMS" type="hidden" value="0"'
            ), 1)
            self.assertEqual(html.count(
                'id="id_form-MAX_NUM_FORMS" name="form-MAX_NUM_FORMS" type="hidden" value="1000"'
            ), 1)
        self.assertEqual(html.count("hidden"), 4)

        # Check form structure
        self.assertEqual(html.count('<form'), 1)
        self.assertEqual(html.count("<input type='hidden' name='csrfmiddlewaretoken'"), 1)
        self.assertTrue('formsets-that-rock' in html)
        self.assertTrue('method="post"' in html)
        self.assertTrue('id="thisFormsetRocks"' in html)
        self.assertTrue('action="%s"' % reverse('simpleAction') in html)

        # Check form layout
        self.assertTrue('Item 1' in html)
        self.assertTrue('Item 2' in html)
        self.assertTrue('Item 3' in html)
        self.assertEqual(html.count('Note for first form only'), 1)
        if self.current_template_pack == 'uni_form':
            self.assertEqual(html.count('formRow'), 3)
        else:
            self.assertEqual(html.count('row'), 3)

    def test_modelformset_layout(self):
        CrispyModelFormSet = modelformset_factory(CrispyTestModel, form=TestForm4, extra=3)
        formset = CrispyModelFormSet(queryset=CrispyTestModel.objects.none())
        helper = FormHelper()
        helper.layout = Layout(
            'email'
        )

        html = render_crispy_form(form=formset, helper=helper)
        self.assertEqual(html.count("id_form-0-id"), 1)
        self.assertEqual(html.count("id_form-1-id"), 1)
        self.assertEqual(html.count("id_form-2-id"), 1)

        django_version = django.get_version()
        if django_version < '1.5':
            self.assertEqual(html.count(
                'type="hidden" name="form-TOTAL_FORMS" value="3" id="id_form-TOTAL_FORMS"'
            ), 1)
            self.assertEqual(html.count(
                'type="hidden" name="form-INITIAL_FORMS" value="0" id="id_form-INITIAL_FORMS"'
            ), 1)
            if (django_version >= '1.4' and django_version < '1.4.4') or django_version < '1.3.6':
                self.assertEqual(html.count(
                    'type="hidden" name="form-MAX_NUM_FORMS" id="id_form-MAX_NUM_FORMS"'
                ), 1)
            else:
                self.assertEqual(html.count(
                    'type="hidden" name="form-MAX_NUM_FORMS" value="1000" id="id_form-MAX_NUM_FORMS"'
                ), 1)
        else:
            self.assertEqual(html.count(
                'id="id_form-TOTAL_FORMS" name="form-TOTAL_FORMS" type="hidden" value="3"'
            ), 1)
            self.assertEqual(html.count(
                'id="id_form-INITIAL_FORMS" name="form-INITIAL_FORMS" type="hidden" value="0"'
            ), 1)
            self.assertEqual(html.count(
                'id="id_form-MAX_NUM_FORMS" name="form-MAX_NUM_FORMS" type="hidden" value="1000"'
            ), 1)

        self.assertEqual(html.count('name="form-0-email"'), 1)
        self.assertEqual(html.count('name="form-1-email"'), 1)
        self.assertEqual(html.count('name="form-2-email"'), 1)
        self.assertEqual(html.count('name="form-3-email"'), 0)
        self.assertEqual(html.count('password'), 0)

    def test_multiwidget_field(self):
        template = loader.get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {% crispy form %}
        """)

        test_form = TestForm()
        test_form.helper = FormHelper()
        test_form.helper.layout = Layout(
            MultiWidgetField(
                'datetime_field',
                attrs=(
                    {'rel': 'test_dateinput'},
                    {'rel': 'test_timeinput', 'style': 'width: 30px;', 'type': "hidden"}
                )
            )
        )

        c = Context({'form': test_form})

        html = template.render(c)
        self.assertEqual(html.count('class="dateinput"'), 1)
        self.assertEqual(html.count('rel="test_dateinput"'), 1)
        self.assertEqual(html.count('rel="test_timeinput"'), 1)
        self.assertEqual(html.count('style="width: 30px;"'), 1)
        self.assertEqual(html.count('type="hidden"'), 1)

    def test_i18n(self):
        template = loader.get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {% crispy form form.helper %}
        """)
        form = TestForm()
        form_helper = FormHelper()
        form_helper.layout = Layout(
            HTML(_("i18n text")),
            Fieldset(
                _("i18n legend"),
                'first_name',
                'last_name',
            )
        )
        form.helper = form_helper

        html = template.render(Context({'form': form}))
        self.assertEqual(html.count('i18n legend'), 1)

    @override_settings(USE_L10N=True, USE_THOUSAND_SEPARATOR=True)
    def test_l10n(self):
        form = TestForm5(data={'pk': 1000})
        html = render_crispy_form(form)

        # Make sure values are unlocalized
        self.assertTrue('value="1,000"' not in html)

        # Make sure label values are NOT localized
        self.assertTrue(html.count('1000'), 2)

    def test_default_layout(self):
        test_form = TestForm2()
        self.assertEqual(test_form.helper.layout.fields,
            ['is_company', 'email', 'password1', 'password2', 'first_name', 'last_name', 'datetime_field']
        )

    def test_default_layout_two(self):
        test_form = TestForm3()
        self.assertEqual(test_form.helper.layout.fields, ['email'])

    def test_modelform_layout_without_meta(self):
        test_form = TestForm4()
        test_form.helper = FormHelper()
        test_form.helper.layout = Layout('email')
        html = render_crispy_form(test_form)

        self.assertTrue('email' in html)
        self.assertFalse('password' in html)

    def test_multiplecheckboxes(self):
        test_form = CheckboxesTestForm()
        html = render_crispy_form(test_form)

        self.assertEqual(html.count('checked="checked"'), 6)

        test_form.helper = FormHelper(test_form)
        test_form.helper[1].wrap(InlineCheckboxes, inline=True)
        html = render_crispy_form(test_form)

        self.assertEqual(html.count('checkbox inline"'), 3)
        self.assertEqual(html.count('inline"'), 3)

    def test_keepcontext_context_manager(self):
        # Test case for issue #180
        # Apparently it only manifest when using render_to_response this exact way
        form = CheckboxesTestForm()
        form.helper = FormHelper()
        # We use here InlineCheckboxes as it updates context in an unsafe way
        form.helper.layout = Layout(
            'checkboxes',
            InlineCheckboxes('alphacheckboxes'),
            'numeric_multiple_checkboxes'
        )
        request_factory = RequestFactory()
        request = request_factory.get('/')
        context = RequestContext(request, {'form': form})

        response = render_to_response('crispy_render_template.html', context)
        self.assertEqual(response.content.count(b'checkbox inline'), 3)


class TestLayoutObjects(CrispyTestCase):
    def test_field_type_hidden(self):
        template = loader.get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {% crispy test_form %}
        """)

        test_form = TestForm()
        test_form.helper = FormHelper()
        test_form.helper.layout = Layout(
            Field('email', type="hidden", data_test=12),
            Field('datetime_field'),
        )

        c = Context({
            'test_form': test_form,
        })
        html = template.render(c)

        # Check form parameters
        self.assertEqual(html.count('data-test="12"'), 1)
        self.assertEqual(html.count('name="email"'), 1)
        self.assertEqual(html.count('class="dateinput"'), 1)
        self.assertEqual(html.count('class="timeinput"'), 1)

    def test_field_wrapper_class(self):
        html = Field('email', wrapper_class="testing").render(TestForm(), "", Context())
        if self.current_template_pack == 'bootstrap':
            self.assertEqual(html.count('class="control-group testing"'), 1)

    def test_custom_django_widget(self):
        class CustomRadioSelect(forms.RadioSelect):
            pass

        class CustomCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
            pass

        if self.current_template_pack == 'bootstrap':
            # Make sure an inherited RadioSelect gets rendered as it
            form = CheckboxesTestForm()
            form.fields['inline_radios'].widget = CustomRadioSelect()
            html = Field('inline_radios').render(form, "", Context())
            self.assertTrue('class="radio"' in html)

            # Make sure an inherited CheckboxSelectMultiple gets rendered as it
            form.fields['checkboxes'].widget = CustomCheckboxSelectMultiple()
            html = Field('checkboxes').render(form, "", Context())
            self.assertTrue('class="checkbox"' in html)

    def test_appended_prepended_text(self):
        test_form = TestForm()
        test_form.helper = FormHelper()
        test_form.helper.layout = Layout(
            AppendedPrependedText('email', '@', 'gmail.com'),
            AppendedText('password1', '#'),
            PrependedText('password2', '$'),
        )
        html = render_crispy_form(test_form)

        # Check form parameters
        self.assertEqual(html.count('<span class="add-on">@</span>'), 1)
        self.assertEqual(html.count('<span class="add-on">gmail.com</span>'), 1)
        self.assertEqual(html.count('<span class="add-on">#</span>'), 1)
        self.assertEqual(html.count('<span class="add-on">$</span>'), 1)

    def test_inline_radios(self):
        test_form = CheckboxesTestForm()
        test_form.helper = FormHelper()
        test_form.helper.layout = Layout(InlineRadios('inline_radios'))
        html = render_crispy_form(test_form)

        self.assertEqual(html.count('radio inline"'), 2)

    def test_accordion_and_accordiongroup(self):
        test_form = TestForm()
        test_form.helper = FormHelper()
        test_form.helper.layout = Layout(
            Accordion(
                AccordionGroup(
                    'one',
                    'first_name'
                ),
                AccordionGroup(
                    'two',
                    'password1',
                    'password2'
                )
            )
        )
        html = render_crispy_form(test_form)

        self.assertEqual(html.count('<div class="accordion"'), 1)
        self.assertEqual(html.count('<div class="accordion-group">'), 2)
        self.assertEqual(html.count('<div id="one"'), 1)
        self.assertEqual(html.count('<div id="two"'), 1)
        self.assertEqual(html.count('name="first_name"'), 1)
        self.assertEqual(html.count('name="password1"'), 1)
        self.assertEqual(html.count('name="password2"'), 1)

    def test_tab_and_tabholder(self):
        test_form = TestForm()
        test_form.helper = FormHelper()
        test_form.helper.layout = Layout(
            TabHolder(
                Tab('one',
                    'first_name',
                    css_id="custom-name"
                ),
                Tab('two',
                    'password1',
                    'password2'
                )
            )
        )
        html = render_crispy_form(test_form)

        self.assertEqual(html.count(
            '<li class="tab-pane active"><a href="#custom-name" data-toggle="tab">One</a></li>'), 1)
        self.assertEqual(html.count('<li class="tab-pane'), 2)
        self.assertEqual(html.count('tab-pane'), 4)
        self.assertEqual(html.count('<div id="custom-name"'), 1)
        self.assertEqual(html.count('<div id="two"'), 1)
        self.assertEqual(html.count('name="first_name"'), 1)
        self.assertEqual(html.count('name="password1"'), 1)
        self.assertEqual(html.count('name="password2"'), 1)

    def test_tab_helper_reuse(self):
        # this is a proper form, according to the docs.
        # note that the helper is a class property here,
        # shared between all instances
        class TestForm(forms.Form):
            val1 = forms.CharField(required=False)
            val2 = forms.CharField(required=True)
            helper = FormHelper()
            helper.layout = Layout(
                TabHolder(Tab('one', 'val1',),
                          Tab('two', 'val2',)))

        # first render of form => everything is fine
        test_form = TestForm()
        html = render_crispy_form(test_form)

        # second render of form => first tab should be active,
        # but not duplicate class
        test_form = TestForm()
        html = render_crispy_form(test_form)
        self.assertEqual(html.count('class="tab-pane active active"'), 0)

        # render a new form, now with errors
        test_form = TestForm(data={'val1': 'foo'})
        html = render_crispy_form(test_form)
        # tab 1 should not be active
        self.assertEqual(html.count('<div id="one" \n    class="tab-pane active'), 0)
        # tab 2 should be active
        self.assertEqual(html.count('<div id="two" \n    class="tab-pane active'), 1)

    def test_html_with_carriage_returns(self):
        test_form = TestForm()
        test_form.helper = FormHelper()
        test_form.helper.layout = Layout(
            HTML("""
                if (a==b){
                    // some comment
                    a+1;
                    foo();
                }
            """)
        )
        html = render_crispy_form(test_form)

        if self.current_template_pack == 'uni_form':
            self.assertEqual(html.count('\n'), 22)
        else:
            self.assertEqual(html.count('\n'), 24)

    def test_radio_attrs(self):
        if self.current_template_pack == 'bootstrap':
            form = CheckboxesTestForm()
            form.fields['inline_radios'].widget.attrs = {'class': "first"}
            form.fields['checkboxes'].widget.attrs = {'class': "second"}
            html = render_crispy_form(form)
            self.assertTrue('class="first"' in html)
            self.assertTrue('class="second"' in html)


class TestDynamicLayouts(CrispyTestCase):
    def setUp(self):
        super(TestDynamicLayouts, self).setUp()

        self.advanced_layout = Layout(
            Div(
                Div(Div('email')),
                Div(Field('password1')),
                Submit("save", "save"),
                Fieldset(
                    "legend",
                    'first_name',
                    HTML("extra text"),
                ),
                Layout(
                    "password2",
                ),
            ),
            'last_name',
        )

    def test_wrap_all_fields(self):
        helper = FormHelper()
        layout = Layout(
            'email',
            'password1',
            'password2',
        )
        helper.layout = layout

        helper.all().wrap(Field, css_class="test-class")
        for field in layout.fields:
            self.assertTrue(isinstance(field, Field))
            self.assertEqual(field.attrs['class'], "test-class")

        self.assertEqual(layout[0][0], 'email')
        self.assertEqual(layout[1][0], 'password1')
        self.assertEqual(layout[2][0], 'password2')

    def test_wrap_selected_fields(self):
        helper = FormHelper()
        layout = Layout(
            'email',
            'password1',
            'password2',
        )
        helper.layout = layout

        helper[1:3].wrap(Field, css_class="test-class")
        self.assertFalse(isinstance(layout.fields[0], Field))
        self.assertTrue(isinstance(layout.fields[1], Field))
        self.assertTrue(isinstance(layout.fields[2], Field))

        helper[0].wrap(Fieldset, 'legend', css_class="test-class")
        self.assertTrue(isinstance(layout[0], Fieldset))
        self.assertEqual(layout[0].legend, 'legend')
        self.assertEqual(layout[0][0], 'email')

    def test_wrap_together_with_slices(self):
        helper = FormHelper()
        layout = Layout(
            'email',
            'password1',
            'password2',
        )
        helper.layout = layout
        helper[1:3].wrap_together(Field, css_class="test-class")
        self.assertEqual(layout.fields[0], 'email')
        self.assertTrue(isinstance(layout.fields[1], Field))
        self.assertEqual(layout.fields[1][0], 'password1')
        self.assertEqual(layout.fields[1][1], 'password2')

        layout = Layout(
            Div('email'),
            'password1',
            'password2',
        )
        helper.layout = layout
        helper[0:3].wrap_together(Field, css_class="test-class")
        self.assertTrue(isinstance(layout.fields[0], Field))
        self.assertTrue(isinstance(layout.fields[0][0], Div))
        self.assertEqual(layout.fields[0][0][0], 'email')
        self.assertEqual(layout.fields[0][1], 'password1')
        self.assertEqual(layout.fields[0][2], 'password2')

        layout = Layout(
            'email',
            'password1',
            'password2',
        )
        helper.layout = layout
        helper[0].wrap_together(Field, css_class="test-class")
        self.assertTrue(isinstance(layout.fields[0], Field))
        self.assertEqual(layout.fields[1], 'password1')
        self.assertEqual(layout.fields[2], 'password2')

        layout = Layout(
            'email',
            'password1',
            'password2',
        )
        helper.layout = layout
        helper[0].wrap_together(Fieldset, "legend", css_class="test-class")
        self.assertTrue(isinstance(layout.fields[0], Fieldset))
        self.assertEqual(layout.fields[0].legend, 'legend')
        self.assertEqual(layout.fields[1], 'password1')
        self.assertEqual(layout.fields[2], 'password2')

    def test_wrap_together_partial_slices(self):
        helper = FormHelper()
        layout = Layout(
            'email',
            'password1',
            'password2',
        )
        helper.layout = layout

        helper[:2].wrap_together(Field, css_class="test-class")
        self.assertTrue(isinstance(layout.fields[0], Field))
        self.assertEqual(layout.fields[1], 'password2')
        self.assertEqual(layout.fields[0][0], 'email')
        self.assertEqual(layout.fields[0][1], 'password1')

        helper = FormHelper()
        layout = Layout(
            'email',
            'password1',
            'password2',
        )
        helper.layout = layout

        helper[1:].wrap_together(Field, css_class="test-class")
        self.assertEqual(layout.fields[0], 'email')
        self.assertTrue(isinstance(layout.fields[1], Field))
        self.assertEqual(layout.fields[1][0], 'password1')
        self.assertEqual(layout.fields[1][1], 'password2')

    def test_update_attributes_and_wrap_once(self):
        helper = FormHelper()
        layout = Layout(
            'email',
            Field('password1'),
            'password2',
        )
        helper.layout = layout
        helper.filter(Field).update_attributes(readonly=True)
        self.assertTrue(isinstance(layout[1], Field))
        self.assertEqual(layout[1].attrs, {'readonly': True})

        layout = Layout(
            'email',
            Div(Field('password1')),
            'password2',
        )
        helper.layout = layout
        helper.filter(Field, max_level=2).update_attributes(readonly=True)
        self.assertTrue(isinstance(layout[1][0], Field))
        self.assertEqual(layout[1][0].attrs, {'readonly': True})

        layout = Layout(
            'email',
            Div(Field('password1')),
            'password2',
        )
        helper.layout = layout

        helper.filter(string_types, greedy=True).wrap_once(Field)
        helper.filter(Field, greedy=True).update_attributes(readonly=True)

        self.assertTrue(isinstance(layout[0], Field))
        self.assertTrue(isinstance(layout[1][0], Field))
        self.assertTrue(isinstance(layout[1][0][0], string_types))
        self.assertTrue(isinstance(layout[2], Field))
        self.assertEqual(layout[1][0].attrs, {'readonly': True})
        self.assertEqual(layout[0].attrs, {'readonly': True})
        self.assertEqual(layout[2].attrs, {'readonly': True})

    def test_get_layout_objects(self):
        layout_1 = Layout(
            Div()
        )
        self.assertEqual(layout_1.get_layout_objects(Div), [
            [[0], 'div']
        ])

        layout_2 = Layout(
            Div(
                Div(
                    Div('email')
                ),
                Div('password1'),
                'password2'
            )
        )
        self.assertEqual(layout_2.get_layout_objects(Div), [
            [[0], 'div']
        ])
        self.assertEqual(layout_2.get_layout_objects(Div, max_level=1), [
            [[0], 'div'],
            [[0, 0], 'div'],
            [[0, 1], 'div']
        ])
        self.assertEqual(layout_2.get_layout_objects(Div, max_level=2), [
            [[0], 'div'],
            [[0, 0], 'div'],
            [[0, 0, 0], 'div'],
            [[0, 1], 'div']
        ])

        layout_3 = Layout(
            'email',
            Div('password1'),
            'password2',
        )
        self.assertEqual(layout_3.get_layout_objects(string_types, max_level=2), [
            [[0], 'email'],
            [[1, 0], 'password1'],
            [[2], 'password2']
        ])

        layout_4 = Layout(
            Div(
                Div('field_name'),
                'field_name2',
            ),
            Div('password'),
            'extra_field'
        )
        self.assertEqual(layout_4.get_layout_objects(Div), [
            [[0], 'div'],
            [[1], 'div']
        ])
        self.assertEqual(layout_4.get_layout_objects(Div, max_level=1), [
            [[0], 'div'],
            [[0, 0], 'div'],
            [[1], 'div']
        ])

    def test_filter(self):
        helper = FormHelper()
        helper.layout = Layout(
            Div(
                MultiField('field_name'),
                'field_name2',
            ),
            Div('password'),
            'extra_field'
        )
        self.assertEqual(helper.filter(Div, MultiField).slice, [
            [[0], 'div'],
            [[1], 'div']
        ])
        self.assertEqual(helper.filter(Div, MultiField, max_level=1).slice, [
            [[0], 'div'],
            [[0, 0], 'multifield'],
            [[1], 'div']
        ])
        self.assertEqual(helper.filter(MultiField, max_level=1).slice, [
            [[0, 0], 'multifield']
        ])

    def test_filter_and_wrap(self):
        helper = FormHelper()
        layout = Layout(
            'email',
            Div('password1'),
            'password2',
        )
        helper.layout = layout

        helper.filter(string_types).wrap(Field, css_class="test-class")
        self.assertTrue(isinstance(layout.fields[0], Field))
        self.assertTrue(isinstance(layout.fields[1], Div))
        self.assertTrue(isinstance(layout.fields[2], Field))
        self.assertEqual(layout[2][0], 'password2')

        # Wrapping a div in a div
        helper.filter(Div).wrap(Div, css_class="test-class")
        self.assertTrue(isinstance(layout.fields[1], Div))
        self.assertTrue(isinstance(layout.fields[1].fields[0], Div))
        self.assertEqual(layout[1][0][0], 'password1')

    def test_filter_and_wrap_side_effects(self):
        helper = FormHelper()
        layout = Layout(
            Div(
                'extra_field',
                Div('password1'),
            ),
        )
        helper.layout = layout
        self.assertRaises(DynamicError, lambda: helper.filter(Div, max_level=2).wrap(Div, css_class="test-class"))

    def test_get_field_names(self):
        layout_1 = Div(
            'field_name'
        )
        self.assertEqual(layout_1.get_field_names(), [
            [[0], 'field_name']
        ])

        layout_2 = Div(
            Div('field_name')
        )
        self.assertEqual(layout_2.get_field_names(), [
            [[0, 0], 'field_name']
        ])

        layout_3 = Div(
            Div('field_name'),
            'password'
        )
        self.assertEqual(layout_3.get_field_names(), [
            [[0, 0], 'field_name'],
            [[1], 'password']
        ])

        layout_4 = Div(
            Div(
                Div('field_name'),
                'field_name2',
            ),
            Div('password'),
            'extra_field'
        )
        self.assertEqual(layout_4.get_field_names(), [
            [[0, 0, 0], 'field_name'],
            [[0, 1], 'field_name2'],
            [[1, 0], 'password'],
            [[2], 'extra_field']
        ])

        layout_5 = Div(
            Div(
                'field_name',
                'field_name2',
            ),
            'extra_field'
        )
        self.assertEqual(layout_5.get_field_names(), [
            [[0, 0], 'field_name'],
            [[0, 1], 'field_name2'],
            [[1], 'extra_field'],
        ])

    def test_layout_get_field_names(self):
        layout_1 = Layout(
            Div('field_name'),
            'password'
        )
        self.assertEqual(layout_1.get_field_names(), [
            [[0, 0], 'field_name'],
            [[1], 'password'],
        ])

        layout_2 = Layout(
            Div('field_name'),
            'password',
            Fieldset('legend', 'extra_field')
        )
        self.assertEqual(layout_2.get_field_names(), [
            [[0, 0], 'field_name'],
            [[1], 'password'],
            [[2, 0], 'extra_field'],
        ])

        layout_3 = Layout(
            Div(
                Div(
                    Div('email')
                ),
                Div('password1'),
                'password2'
            )
        )
        self.assertEqual(layout_3.get_field_names(), [
            [[0, 0, 0, 0], 'email'],
            [[0, 1, 0], 'password1'],
            [[0, 2], 'password2'],
        ])

    def test_filter_by_widget(self):
        form = TestForm()
        form.helper = FormHelper(form)
        form.helper.layout = self.advanced_layout
        self.assertEqual(form.helper.filter_by_widget(forms.PasswordInput).slice, [
            [[0, 1, 0, 0], 'password1'],
            [[0, 4, 0], 'password2'],
        ])

    def test_exclude_by_widget(self):
        form = TestForm()
        form.helper = FormHelper(form)
        form.helper.layout = self.advanced_layout
        self.assertEqual(form.helper.exclude_by_widget(forms.PasswordInput).slice, [
            [[0, 0, 0, 0], 'email'],
            [[0, 3, 0], 'first_name'],
            [[1], 'last_name'],
        ])

    def test_exclude_by_widget_and_wrap(self):
        form = TestForm()
        form.helper = FormHelper(form)
        form.helper.layout = self.advanced_layout
        form.helper.exclude_by_widget(forms.PasswordInput).wrap(Field, css_class='hero')
        # Check wrapped fields
        self.assertTrue(isinstance(form.helper.layout[0][0][0][0], Field))
        self.assertTrue(isinstance(form.helper.layout[0][3][0], Field))
        self.assertTrue(isinstance(form.helper.layout[1], Field))
        # Check others stay the same
        self.assertTrue(isinstance(form.helper.layout[0][3][1], HTML))
        self.assertTrue(isinstance(form.helper.layout[0][1][0][0], string_types))
        self.assertTrue(isinstance(form.helper.layout[0][4][0], string_types))

    def test_all_without_layout(self):
        form = TestForm()
        form.helper = FormHelper()
        self.assertRaises(FormHelpersException, lambda: form.helper.all().wrap(Div))

    def test_filter_by_widget_without_form(self):
        form = TestForm()
        form.helper = FormHelper()
        form.helper.layout = self.advanced_layout
        self.assertRaises(FormHelpersException, lambda: form.helper.filter_by_widget(forms.PasswordInput))

    def test_formhelper__getitem__(self):
        helper = FormHelper()
        layout = Layout(
            Div('email'),
            'password1',
        )
        helper.layout = layout
        helper['email'].wrap(Field, css_class='hero')
        self.assertTrue(isinstance(layout[0][0], Field))
        self.assertEqual(layout[0][0][0], 'email')

        helper = FormHelper()
        helper.layout = Layout('password1')
        helper['password1'].wrap(AppendedText, "extra")
        self.assertTrue(isinstance(helper.layout[0], AppendedText))
        self.assertEqual(helper.layout[0][0], 'password1')
        self.assertEqual(helper.layout[0].text, 'extra')

    def test_formhelper__setitem__(self):
        helper = FormHelper()
        layout = Layout(
            'first_field',
            Div('email')
        )
        helper.layout = layout
        helper[0] = 'replaced'
        self.assertEqual(layout[0], 'replaced')

    def test_formhelper__delitem__and__len__(self):
        helper = FormHelper()
        layout = Layout(
            'first_field',
            Div('email')
        )
        helper.layout = layout
        del helper[0]
        self.assertEqual(len(helper), 1)

    def test__delitem__and__len__layout_object(self):
        layout = Layout(
            'first_field',
            Div('email')
        )
        del layout[0]
        self.assertEqual(len(layout), 1)

    def test__getitem__layout_object(self):
        layout = Layout(
            Div(
                Div(
                    Div('email')
                ),
                Div('password1'),
                'password2'
            )
        )
        self.assertTrue(isinstance(layout[0], Div))
        self.assertTrue(isinstance(layout[0][0], Div))
        self.assertTrue(isinstance(layout[0][0][0], Div))
        self.assertTrue(isinstance(layout[0][1], Div))
        self.assertTrue(isinstance(layout[0][1][0], string_types))
        self.assertTrue(isinstance(layout[0][2], string_types))

    def test__getattr__append_layout_object(self):
        layout = Layout(
            Div('email')
        )
        layout.append('password1')
        self.assertTrue(isinstance(layout[0], Div))
        self.assertTrue(isinstance(layout[0][0], string_types))
        self.assertTrue(isinstance(layout[1], string_types))

    def test__setitem__layout_object(self):
        layout = Layout(
            Div('email')
        )
        layout[0][0] = 'password1'
        self.assertTrue(isinstance(layout[0], Div))
        self.assertEqual(layout[0][0], 'password1')
