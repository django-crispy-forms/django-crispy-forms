# -*- coding: utf-8 -*-
from django.conf import settings
from django.forms.forms import BoundField
from django.forms.models import formset_factory
from django.template import loader, Context

from .base import CrispyTestCase
from .forms import TestForm
from crispy_forms.templatetags.crispy_forms_field import crispy_addon



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

        TestFormset = formset_factory(TestForm, extra=4)
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

        if self.current_template_pack == 'bootstrap':
            # prepend tests
            self.assertIn("input-prepend", crispy_addon(bound_field, prepend="Work"))
            self.assertNotIn("input-append", crispy_addon(bound_field, prepend="Work"))
            # append tests
            self.assertNotIn("input-prepend", crispy_addon(bound_field, append="Primary"))
            self.assertIn("input-append", crispy_addon(bound_field, append="Secondary"))
            # prepend and append tests
            self.assertIn("input-append", crispy_addon(bound_field, prepend="Work", append="Primary"))
            self.assertIn("input-prepend", crispy_addon(bound_field, prepend="Work", append="Secondary"))
        elif self.current_template_pack == 'bootsrap3':
            self.assertIn("input-group-addon", crispy_addon(bound_field, prepend="Work", append="Primary"))
            self.assertIn("input-group-addon", crispy_addon(bound_field, prepend="Work", append="Secondary"))

        # errors
        with self.assertRaises(TypeError):
            crispy_addon()
            crispy_addon(bound_field)
