# -*- coding: utf-8 -*-
import django
from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse
from django.forms.models import formset_factory
from django.template import Context, TemplateSyntaxError
from django.template.loader import get_template_from_string
from django.middleware.csrf import _get_new_csrf_key
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper, FormHelpersException
from crispy_forms.layout import Submit, Reset, Hidden, Button
from crispy_forms.layout import (
    Layout, Fieldset, MultiField, Row, Column, HTML, ButtonHolder,
    Div, Field, MultiWidgetField
)
from crispy_forms.bootstrap import (
    AppendedPrependedText, AppendedText, PrependedText
)
from forms import (
    TestForm, TestForm2, TestForm3, ExampleForm
)


class TestBasicFunctionalityTags(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_as_crispy_errors_form_without_non_field_errors(self):
        template = get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {{ form|as_crispy_errors }}
        """)
        form = TestForm({'password1': "god", 'password2': "god"})
        form.is_valid()

        c = Context({'form': form})
        html = template.render(c)
        self.assertFalse("errorMsg" in html or "alert" in html)

    def test_as_crispy_errors_form_with_non_field_errors(self):
        template = get_template_from_string(u"""
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
        template = get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {{ form|crispy }}
        """)
        c = Context({'form': TestForm()})
        html = template.render(c)

        self.assertTrue("<td>" not in html)
        self.assertTrue("id_is_company" in html)

    def test_crispy_filter_with_formset(self):
        template = get_template_from_string(u"""
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
        template = get_template_from_string(u"""
            {% load crispy_forms_field %}
            {{ testField|classes }}
        """)

        test_form = TestForm()
        test_form.fields['email'].widget.attrs.update({'class': 'email-fields'})
        c = Context({'testField': test_form.fields['email']})
        html = template.render(c)
        self.assertTrue('email-fields' in html)


class TestFormHelpers(TestCase):
    urls = 'crispy_forms.tests.urls'
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_crispy_tag_helper_inputs(self):
        form_helper = FormHelper()
        submit  = Submit('my-submit', 'Submit', css_class="button white")
        reset   = Reset('my-reset', 'Reset')
        hidden  = Hidden('my-hidden', 'Hidden')
        button  = Button('my-button', 'Button')
        form_helper.add_input(submit)
        form_helper.add_input(reset)
        form_helper.add_input(hidden)
        form_helper.add_input(button)

        template = get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {% crispy form form_helper %}
        """)
        c = Context({'form': TestForm(), 'form_helper': form_helper})
        html = template.render(c)

        self.assertTrue('button white' in html)
        self.assertTrue('submit submitButton' in html or 'btn' in html)
        self.assertTrue('id="submit-id-my-submit"' in html)

        self.assertTrue('reset resetButton' in html)
        self.assertTrue('id="reset-id-my-reset"' in html)

        self.assertTrue('name="my-hidden"' in html)

        self.assertTrue('button' in html)
        self.assertTrue('id="button-id-my-button"' in html)

    def test_invalid_helper_method(self):
        form_helper = FormHelper()
        try:
            form_helper.form_method = "superPost"
            self.fail("Setting an invalid form_method within the helper should raise an Exception")
        except FormHelpersException:
            pass

    def test_crispy_tag_with_helper_without_layout(self):
        form_helper = FormHelper()
        form_helper.form_id = 'this-form-rocks'
        form_helper.form_class = 'forms-that-rock'
        form_helper.form_method = 'GET'
        form_helper.form_action = 'simpleAction'
        form_helper.form_error_title = 'ERRORS'

        template = get_template_from_string(u"""
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
        self.assertTrue('id="this-form-rocks">' in html)
        self.assertTrue('action="%s"' % reverse('simpleAction') in html)

        self.assertTrue("ERRORS" in html)
        self.assertTrue("<li>Passwords dont match</li>" in html)

        # now lets remove the form tag and render it again. All the True items above
        # should now be false because the form tag is removed.
        form_helper.form_tag = False
        html = template.render(c)
        self.assertFalse('<form' in html)
        self.assertFalse('forms-that-rock' in html)
        self.assertFalse('method="get"' in html)
        self.assertFalse('id="this-form-rocks">' in html)

    def test_crispy_tag_with_helper_form_show_errors(self):
        form = TestForm({'password1': 'wargame', 'password2': 'god'})
        form.helper = FormHelper()
        form.helper.form_show_errors = True
        form.is_valid()

        template = get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {% crispy testForm %}
        """)

        # First we render with errors
        c = Context({'testForm': form})
        html = template.render(c)

        # Ensure those errors were rendered
        self.assertTrue('<li>Passwords dont match</li>' in html)
        self.assertTrue(unicode(_('This field is required.')) in html)
        self.assertTrue('error' in html)

        # Now we render without errors
        form.helper.form_show_errors = False
        c = Context({'testForm': form})
        html = template.render(c)

        # Ensure errors were not rendered
        self.assertFalse('<li>Passwords dont match</li>' in html)
        self.assertFalse(unicode(_('This field is required.')) in html)
        self.assertFalse('error' in html)

    def test_crispy_tag_without_helper(self):
        template = get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {% crispy form %}
        """)
        c = Context({'form': TestForm()})
        html = template.render(c)

        # Lets make sure everything loads right
        self.assertTrue('<form' in html)
        self.assertTrue('method="post"' in html)
        self.assertFalse('action' in html)

    def test_crispy_tag_invalid_helper(self):
        template = get_template_from_string(u"""
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

    def test_crispy_tag_formset_with_helper_without_layout(self):
        template = get_template_from_string(u"""
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
        self.assertTrue('id="thisFormsetRocks">' in html)
        self.assertTrue('action="%s"' % reverse('simpleAction') in html)

    def test_CSRF_token_POST_form(self):
        form_helper = FormHelper()
        template = get_template_from_string(u"""
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
        template = get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {% crispy form form_helper %}
        """)

        c = Context({'form': TestForm(), 'form_helper': form_helper, 'csrf_token': _get_new_csrf_key()})
        html = template.render(c)

        self.assertFalse("<input type='hidden' name='csrfmiddlewaretoken'" in html)


class TestFormLayout(TestCase):
    urls = 'crispy_forms.tests.urls'
    def test_layout_invalid_unicode_characters(self):
        # Adds a BooleanField that uses non valid unicode characters "ñ"
        form_helper = FormHelper()
        form_helper.add_layout(
            Layout(
                'españa'
            )
        )

        template = get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {% crispy form form_helper %}
        """)
        c = Context({'form': TestForm(), 'form_helper': form_helper})
        settings.CRISPY_FAIL_SILENTLY = False
        self.assertRaises(Exception, lambda:template.render(c))
        del settings.CRISPY_FAIL_SILENTLY

    def test_layout_uses_instance_for_missing_fields(self):
        class FormWithMeta(TestForm):
            class Meta:
                fields = ('email', 'first_name', 'last_name')
        form = FormWithMeta()
        # We remove email field on the go
        del form.fields['email']

        form_helper = FormHelper()
        form_helper.add_layout(
            Layout(
                'first_name',
            )
        )

        template = get_template_from_string(u"""
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

        template = get_template_from_string(u"""
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

        template = get_template_from_string(u"""
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

        template = get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {{ form.as_ul }}
            {% crispy form2 %}
            {{ form.as_ul }}
        """)
        c = Context({'form': form, 'form2': form2})
        html = template.render(c)

        self.assertEqual(html.count('<input type="text" name="comment"'), 2)
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

        template = get_template_from_string(u"""
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
        self.assertTrue('class="formRow rows"' in html)
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
                    Submit('Save the world', 'Save', css_class='button white', data_id='test', data_name='test'),
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

        template = get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {% crispy form form_helper %}
        """)
        c = Context({'form': TestForm(), 'form_helper': form_helper})
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

        template = get_template_from_string(u"""
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
        template = get_template_from_string(u"""
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
        template = get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {% crispy testFormSet formset_helper %}
        """)

        form_helper = FormHelper()
        form_helper.form_id = 'thisFormsetRocks'
        form_helper.form_class = 'formsets-that-rock'
        form_helper.form_method = 'POST'
        form_helper.form_action = 'simpleAction'
        form_helper.add_layout(
            Layout(
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
        )

        TestFormSet = formset_factory(TestForm, extra = 3)
        testFormSet = TestFormSet()

        c = Context({
            'testFormSet': testFormSet,
            'formset_helper': form_helper,
            'csrf_token': _get_new_csrf_key()
        })
        html = template.render(c)

        # Check form parameters
        self.assertEqual(html.count('<form'), 1)
        self.assertEqual(html.count("<input type='hidden' name='csrfmiddlewaretoken'"), 1)

        self.assertTrue('formsets-that-rock' in html)
        self.assertTrue('method="post"' in html)
        self.assertTrue('id="thisFormsetRocks">' in html)
        self.assertTrue('action="%s"' % reverse('simpleAction') in html)

        # Check form layout
        self.assertTrue('Item 1' in html)
        self.assertTrue('Item 2' in html)
        self.assertTrue('Item 3' in html)
        self.assertEqual(html.count('Note for first form only'), 1)
        self.assertEqual(html.count('formRow'), 3)

    def test_multiwidget_field(self):
        template = get_template_from_string(u"""
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
        template = get_template_from_string(u"""
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

    def test_default_layout(self):
        test_form = TestForm2()
        self.assertEqual(test_form.helper.layout.fields,
            ['is_company', 'email', 'password1', 'password2', 'first_name', 'last_name', 'datetime_field']
        )

    def test_default_layout_two(self):
        test_form = TestForm3()
        self.assertEqual(test_form.helper.layout.fields, ['email'])


class TestLayoutObjects(TestCase):
    def test_field_type_hidden(self):
        template = get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {% crispy test_form %}
        """)


        test_form = TestForm()
        test_form.helper = FormHelper()
        test_form.helper.layout = Layout(
            Field('email', type="hidden", data_mierda=12),
            Field('datetime_field'),
        )

        c = Context({
            'test_form': test_form,
        })
        html = template.render(c)

        # Check form parameters
        self.assertEqual(html.count('<input type="hidden" data-mierda="12" name="email"'), 1)
        self.assertEqual(html.count('class="dateinput"'), 1)
        self.assertEqual(html.count('class="timeinput"'), 1)

    def test_appended_prepended_text(self):
        template = get_template_from_string(u"""
            {% load crispy_forms_tags %}
            {% crispy test_form %}
        """)

        test_form = TestForm()
        test_form.helper = FormHelper()
        test_form.helper.layout = Layout(
            AppendedPrependedText('email', '@', 'gmail.com'),
            AppendedText('password1', '#'),
            PrependedText('password2', '$'),
        )

        c = Context({
            'test_form': test_form,
        })
        html = template.render(c)

        # Check form parameters
        self.assertEqual(html.count('<span class="add-on ">@</span>'), 1)
        self.assertEqual(html.count('<span class="add-on ">gmail.com</span>'), 1)
        self.assertEqual(html.count('<span class="add-on ">#</span>'), 1)
        self.assertEqual(html.count('<span class="add-on ">$</span>'), 1)


class TestDynamicLayouts(TestCase):
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

        helper[0].wrap(Field, css_class="test-class")
        self.assertTrue(isinstance(layout.fields[0], Field))

    def test_wrap_filtered_fields(self):
        helper = FormHelper()
        layout = Layout(
            'email',
            Div('password1'),
            'password2',
        )
        helper.layout = layout

        helper.filter(basestring).wrap(Field, css_class="test-class")
        self.assertTrue(isinstance(layout.fields[0], Field))
        self.assertTrue(isinstance(layout.fields[1], Div))
        self.assertTrue(isinstance(layout.fields[2], Field))

        # Wrapping a div in a div
        helper.filter(Div).wrap(Div, css_class="test-class")
        self.assertTrue(isinstance(layout.fields[1], Div))
        self.assertTrue(isinstance(layout.fields[1].fields[0], Div))

    def test_get_field_names(self):
        layout_1 = Div('field_name')
        self.assertEqual(layout_1.get_field_names(), [[0], 'field_name'])

        layout_2 = Div(
            Div('field_name')
        )
        self.assertEqual(layout_2.get_field_names(), [[0, 0], 'field_name'])

        layout_3 = Div(
            Div('field_name'),
            'password'
        )
        self.assertEqual(layout_3.get_field_names(), [
            [[0, 0], 'field_name'],
            [[1], 'password']
        ])

        layout_4 = Div(
            Div(Div('field_name')),
            Div('password'),
            'extra_field'
        )
        self.assertEqual(layout_4.get_field_names(), [
            [[0, 0, 0], 'field_name'],
            [[1, 0], 'password'],
            [[2], 'extra_field']
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
        layout = Layout(
            Div(
                Div(Div('email')),
                Div('password1'),
                'password2'
            )
        )
        form.helper.layout = layout
        form.helper.filter_by_widget(forms.PasswordInput).wrap(Field, css_class='hero')
        self.assertTrue(isinstance(layout.fields[0].fields[2], Field))

    def test_getitem_by_field_name(self):
        form = TestForm()
        form.helper = FormHelper(form)
        layout = Layout(
            Div('email'),
            'password1',
        )
        form.helper.layout = layout
        form.helper['email'].wrap(Field, css_class='hero')
        self.assertTrue(isinstance(layout.fields[0].fields[0], Field))

    def test_getitem_layout_object(self):
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
        self.assertTrue(isinstance(layout[0][1][0], basestring))
        self.assertTrue(isinstance(layout[0][2], basestring))

    def test_append_layout_object(self):
        layout = Layout(
            Div('email')
        )
        layout.append('password1')
        self.assertTrue(isinstance(layout[0], Div))
        self.assertTrue(isinstance(layout[0][0], basestring))
        self.assertTrue(isinstance(layout[1], basestring))

    def test_setitem_layout_object(self):
        layout = Layout(
            Div('email')
        )
        layout[0][0] = 'password1'
        self.assertTrue(isinstance(layout[0], Div))
        self.assertEqual(layout[0][0], 'password1')
