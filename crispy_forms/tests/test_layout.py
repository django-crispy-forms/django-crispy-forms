# -*- coding: utf-8 -*-
import re

import django, logging, warnings
from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse
from django.forms.models import formset_factory, modelformset_factory
from django.middleware.csrf import _get_new_csrf_key
from django.shortcuts import render_to_response
from django.template import (
    Context, RequestContext, loader
)
from django.test import RequestFactory
from django.utils.translation import ugettext_lazy as _

from .base import CrispyTestCase
from .forms import (
    TestForm, TestForm2, TestForm3, CheckboxesTestForm,
    TestForm4, CrispyTestModel, TestForm5
)
from .utils import override_settings
from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.compatibility import PY2
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout, Fieldset, MultiField, Row, Column, HTML, ButtonHolder,
    Div, Submit
)
from crispy_forms.utils import render_crispy_form

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
        self.assertRaises(Exception, lambda: template.render(c))
        del settings.CRISPY_FAIL_SILENTLY

    def test_unicode_form_field(self):
        class UnicodeForm(forms.Form):
            def __init__(self, *args, **kwargs):
                super(UnicodeForm, self).__init__(*args, **kwargs)
                self.fields['contraseña'] = forms.CharField()

            helper = FormHelper()
            helper.layout = Layout(u'contraseña')

        if PY2:
            self.assertRaises(Exception, lambda: render_crispy_form(UnicodeForm()))
        else:
            html = render_crispy_form(UnicodeForm())
            self.assertTrue('id="id_contraseña"' in html)

    def test_meta_extra_fields_with_missing_fields(self):
        class FormWithMeta(TestForm):
            class Meta:
                fields = ('email', 'first_name', 'last_name')

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
                'is_company',
                'is_company',
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
        class ExampleForm(forms.Form):
            comment = forms.CharField()

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
        django_version = django.VERSION[:3]
        hidden_count = 4  # before Django 1.7 added MIN_NUM_FORM_COUNT
        if django_version < (1, 5):
            self.assertEqual(html.count(
                'type="hidden" name="form-TOTAL_FORMS" value="3" id="id_form-TOTAL_FORMS"'
            ), 1)
            self.assertEqual(html.count(
                'type="hidden" name="form-INITIAL_FORMS" value="0" id="id_form-INITIAL_FORMS"'
            ), 1)
            if (django_version >= (1, 4) and django_version < (1, 4, 4)) or django_version < (1, 3, 6):
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
            if hasattr(forms.formsets, 'MIN_NUM_FORM_COUNT'):
                self.assertEqual(html.count(
                    'id="id_form-MIN_NUM_FORMS" name="form-MIN_NUM_FORMS" type="hidden" value="0"'
                ), 1)
                hidden_count += 1
        self.assertEqual(html.count("hidden"), hidden_count)

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

        django_version = django.VERSION[:3]
        if django_version < (1, 5):
            self.assertEqual(html.count(
                'type="hidden" name="form-TOTAL_FORMS" value="3" id="id_form-TOTAL_FORMS"'
            ), 1)
            self.assertEqual(html.count(
                'type="hidden" name="form-INITIAL_FORMS" value="0" id="id_form-INITIAL_FORMS"'
            ), 1)
            if (django_version >= (1, 4) and django_version < (1, 4, 4)) or django_version < (1, 3, 6):
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
        self.assertEqual(test_form.helper.layout.fields, [
            'is_company', 'email', 'password1', 'password2',
            'first_name', 'last_name', 'datetime_field',
        ])

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

    def test_specialspaceless_not_screwing_intended_spaces(self):
        # see issue #250
        test_form = TestForm()
        test_form.fields['email'].widget = forms.Textarea()
        test_form.helper = FormHelper()
        test_form.helper.layout = Layout(
            'email',
            HTML("<span>first span</span> <span>second span</span>")
        )
        html = render_crispy_form(test_form)
        self.assertTrue('<span>first span</span> <span>second span</span>' in html)


class TestUniformFormLayout(TestFormLayout):

    def test_layout_composition(self):
        if settings.CRISPY_TEMPLATE_PACK != 'uni_form':
            warnings.warn('skipping uniform tests with CRISPY_TEMPLATE_PACK=%s' % settings.CRISPY_TEMPLATE_PACK)
            return
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

    def test_second_layout_multifield_column_buttonholder_submit_div(self):
        if settings.CRISPY_TEMPLATE_PACK != 'uni_form':
            warnings.warn('skipping uniform tests with CRISPY_TEMPLATE_PACK=%s' % settings.CRISPY_TEMPLATE_PACK)
            return
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


class TestBootstrapFormLayout(TestFormLayout):

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

        if self.current_template_pack == 'bootstrap':
            self.assertEqual(response.content.count(b'checkbox inline'), 3)
        elif self.current_template_pack == 'bootstrap3':
            self.assertEqual(response.content.count(b'checkbox-inline'), 3)


class TestBootstrap3FormLayout(TestFormLayout):

    def test_form_inline(self):
        form = TestForm()
        form.helper = FormHelper()
        form.helper.form_class = 'form-inline'
        form.helper.field_template = 'bootstrap3/layout/inline_field.html'
        form.helper.layout = Layout(
            'email',
            'password1',
            'last_name',
        )

        html = render_crispy_form(form)
        self.assertEqual(html.count('class="form-inline"'), 1)
        self.assertEqual(html.count('class="form-group"'), 3)
        self.assertEqual(html.count('<label for="id_email" class="sr-only'), 1)
        self.assertEqual(html.count('id="div_id_email" class="form-group"'), 1)
        self.assertEqual(html.count('placeholder="email"'), 1)
        self.assertEqual(html.count('</label> <input'), 3)
