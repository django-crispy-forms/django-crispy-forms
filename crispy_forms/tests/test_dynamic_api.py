# -*- coding: utf-8 -*-
from django import forms

from .base import CrispyTestCase
from crispy_forms.compatibility import string_types
from crispy_forms.exceptions import DynamicError
from crispy_forms.helper import FormHelper, FormHelpersException
from crispy_forms.layout import Submit
from crispy_forms.layout import (
    Layout, Fieldset, MultiField, HTML, Div, Field
)
from crispy_forms.bootstrap import AppendedText
from crispy_forms.tests.forms import TestForm


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

    def test_update_attributes(self):
        helper = FormHelper()
        helper.layout = Layout(
            'email',
            Field('password1'),
            'password2',
        )
        helper['password1'].update_attributes(readonly=True)
        self.assertTrue('readonly' in helper.layout[1].attrs)

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
