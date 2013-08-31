# -*- coding: utf-8 -*-
import re

import django
from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse
from django.forms.models import formset_factory
from django.middleware.csrf import _get_new_csrf_key
from django.template import (
    loader, TemplateSyntaxError, Context
)
from django.utils.translation import ugettext_lazy as _

from .base import CrispyTestCase
from .forms import TestForm
from crispy_forms.bootstrap import (
    FieldWithButtons, PrependedAppendedText, AppendedText, PrependedText,
    StrictButton
)
from crispy_forms.compatibility import text_type
from crispy_forms.helper import FormHelper, FormHelpersException
from crispy_forms.layout import (
    Layout, Submit, Reset, Hidden, Button, MultiField,
)
from crispy_forms.utils import render_crispy_form
from crispy_forms.templatetags.crispy_forms_tags import CrispyFormNode


class TestFormHelper(CrispyTestCase):
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



class TestBootstrapFormHelper(CrispyTestCase):
    urls = 'crispy_forms.tests.urls'

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
            PrependedAppendedText('last_name', 'foo', 'bar'),
            MultiField('legend', 'password1', 'password2')
        )
        form.is_valid()

        form.helper.form_show_errors = True
        html = render_crispy_form(form)
        self.assertEqual(html.count('error'), 6)

        form.helper.form_show_errors = False
        html = render_crispy_form(form)
        self.assertEqual(html.count('error'), 0)

    def test_error_text_inline(self):
        form = TestForm({'email': 'invalidemail'})
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
        if self.current_template_pack == 'bootstrap3':
            help_class = 'help-block'

        matches = re.findall(
            '<span id="error_\d_\w*" class="%s"' % help_class, html, re.MULTILINE
        )
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
        error_position = html.find('<span id="error_1_id_email" class="help-inline">')
        help_position = html.find('<p id="hint_id_email" class="help-block">')
        self.assertTrue(error_position < help_position)

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
            PrependedAppendedText(
                'datetime_field',
                'on',
                'secs'
            )
        )
        form.helper.form_show_labels = False

        html = render_crispy_form(form)
        self.assertEqual(html.count("<label"), 0)
