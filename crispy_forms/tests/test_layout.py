# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.core.urlresolvers import reverse
from django.forms.models import formset_factory, modelformset_factory
try:
    from django.middleware.csrf import _get_new_csrf_key
except ImportError:
    from django.middleware.csrf import _get_new_csrf_string as _get_new_csrf_key
from django.shortcuts import render_to_response
from django.template import (
    Context, RequestContext
)
import pytest

from django.test import RequestFactory
from django.utils.translation import ugettext_lazy as _

from .compatibility import get_template_from_string
from .conftest import only_uni_form, only_bootstrap3, only_bootstrap4, only_bootstrap
from .forms import (
    TestForm, TestForm2, TestForm3, CheckboxesTestForm,
    TestForm4, CrispyTestModel, TestForm5
)
from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.compatibility import PY2
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout, Fieldset, MultiField, Row, Column, HTML, ButtonHolder,
    Div, Submit
)
from crispy_forms.utils import render_crispy_form


def test_invalid_unicode_characters(settings):
    # Adds a BooleanField that uses non valid unicode characters "ñ"
    form_helper = FormHelper()
    form_helper.add_layout(
        Layout(
            'españa'
        )
    )

    template = get_template_from_string("""
        {% load crispy_forms_tags %}
        {% crispy form form_helper %}
    """)
    c = Context({'form': TestForm(), 'form_helper': form_helper})
    settings.CRISPY_FAIL_SILENTLY = False
    with pytest.raises(Exception):
        template.render(c)


def test_unicode_form_field():
    class UnicodeForm(forms.Form):
        def __init__(self, *args, **kwargs):
            super(UnicodeForm, self).__init__(*args, **kwargs)
            self.fields['contraseña'] = forms.CharField()

        helper = FormHelper()
        helper.layout = Layout('contraseña')

    if PY2:
        with pytest.raises(Exception):
            render_crispy_form(UnicodeForm())
    else:
        html = render_crispy_form(UnicodeForm())
        assert 'id="id_contraseña"' in html


def test_meta_extra_fields_with_missing_fields():
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

    template = get_template_from_string("""
        {% load crispy_forms_tags %}
        {% crispy form form_helper %}
    """)
    c = Context({'form': form, 'form_helper': form_helper})
    html = template.render(c)
    assert 'email' not in html


def test_layout_unresolved_field(settings):
    form_helper = FormHelper()
    form_helper.add_layout(
        Layout(
            'typo'
        )
    )

    template = get_template_from_string("""
        {% load crispy_forms_tags %}
        {% crispy form form_helper %}
    """)
    c = Context({'form': TestForm(), 'form_helper': form_helper})
    settings.CRISPY_FAIL_SILENTLY = False
    with pytest.raises(Exception):
        template.render(c)


def test_double_rendered_field(settings):
    form_helper = FormHelper()
    form_helper.add_layout(
        Layout(
            'is_company',
            'is_company',
        )
    )

    template = get_template_from_string("""
        {% load crispy_forms_tags %}
        {% crispy form form_helper %}
    """)
    c = Context({'form': TestForm(), 'form_helper': form_helper})
    settings.CRISPY_FAIL_SILENTLY = False
    with pytest.raises(Exception):
        template.render(c)


def test_context_pollution():
    class ExampleForm(forms.Form):
        comment = forms.CharField()

    form = ExampleForm()
    form2 = TestForm()

    template = get_template_from_string("""
        {% load crispy_forms_tags %}
        {{ form.as_ul }}
        {% crispy form2 %}
        {{ form.as_ul }}
    """)
    c = Context({'form': form, 'form2': form2})
    html = template.render(c)

    assert html.count('name="comment"') == 2
    assert html.count('name="is_company"') == 1


def test_layout_fieldset_row_html_with_unicode_fieldnames(settings):
    form_helper = FormHelper()
    form_helper.add_layout(
        Layout(
            Fieldset(
                'Company Data',
                'is_company',
                css_id="fieldset_company_data",
                css_class="fieldsets",
                title="fieldset_title",
                test_fieldset="123"
            ),
            Fieldset(
                'User Data',
                'email',
                Row(
                    'password1',
                    'password2',
                    css_id="row_passwords",
                    css_class="rows",
                ),
                HTML('<a href="#" id="testLink">test link</a>'),
                HTML("""
                    {% if flag %}{{ message }}{% endif %}
                """),
                'first_name',
                'last_name',
            )
        )
    )

    template = get_template_from_string("""
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

    assert 'id="fieldset_company_data"' in html
    assert 'class="fieldsets' in html
    assert 'title="fieldset_title"' in html
    assert 'test-fieldset="123"' in html
    assert 'id="row_passwords"' in html
    assert html.count('<label') == 6

    if settings.CRISPY_TEMPLATE_PACK == 'uni_form':
        assert 'class="formRow rows"' in html
    else:
        assert 'class="row rows"' in html
    assert 'Hello!' in html
    assert 'testLink' in html


def test_change_layout_dynamically_delete_field():
    template = get_template_from_string("""
        {% load crispy_forms_tags %}
        {% crispy form form_helper %}
    """)

    form = TestForm()
    form_helper = FormHelper()
    form_helper.add_layout(
        Layout(
            Fieldset(
                'Company Data',
                'is_company',
                'email',
                'password1',
                'password2',
                css_id="multifield_info",
            ),
            Column(
                'first_name',
                'last_name',
                css_id="column_name",
            )
        )
    )

    # We remove email field on the go
    # Layout needs to be adapted for the new form fields
    del form.fields['email']
    del form_helper.layout.fields[0].fields[1]

    c = Context({'form': form, 'form_helper': form_helper})
    html = template.render(c)
    assert 'email' not in html


def test_formset_layout(settings):
    TestFormSet = formset_factory(TestForm, extra=3)
    formset = TestFormSet()
    helper = FormHelper()
    helper.form_id = 'thisFormsetRocks'
    helper.form_class = 'formsets-that-rock'
    helper.form_method = 'POST'
    helper.form_action = 'simpleAction'
    helper.layout = Layout(
        Fieldset(
            "Item {{ forloop.counter }}",
            'is_company',
            'email',
        ),
        HTML("{% if forloop.first %}Note for first form only{% endif %}"),
        Row('password1', 'password2'),
        Fieldset(
            "",
            'first_name',
            'last_name'
        )
    )

    html = render_crispy_form(
        form=formset, helper=helper, context={'csrf_token': _get_new_csrf_key()}
    )

    # Check formset fields
    hidden_count = 4  # before Django 1.7 added MIN_NUM_FORM_COUNT
    assert html.count(
        'id="id_form-TOTAL_FORMS" name="form-TOTAL_FORMS" type="hidden" value="3"'
    ) == 1
    assert html.count(
        'id="id_form-INITIAL_FORMS" name="form-INITIAL_FORMS" type="hidden" value="0"'
    ) == 1
    assert html.count(
        'id="id_form-MAX_NUM_FORMS" name="form-MAX_NUM_FORMS" type="hidden" value="1000"'
    ) == 1
    if hasattr(forms.formsets, 'MIN_NUM_FORM_COUNT'):
        assert html.count(
            'id="id_form-MIN_NUM_FORMS" name="form-MIN_NUM_FORMS" type="hidden" value="0"'
        ) == 1
        hidden_count += 1
    assert html.count("hidden") == hidden_count

    # Check form structure
    assert html.count('<form') == 1
    assert html.count("<input type='hidden' name='csrfmiddlewaretoken'") == 1
    assert 'formsets-that-rock' in html
    assert 'method="post"' in html
    assert 'id="thisFormsetRocks"' in html
    assert 'action="%s"' % reverse('simpleAction') in html

    # Check form layout
    assert 'Item 1' in html
    assert 'Item 2' in html
    assert 'Item 3' in html
    assert html.count('Note for first form only') == 1
    if settings.CRISPY_TEMPLATE_PACK == 'uni_form':
        assert html.count('formRow') == 3
    else:
        assert html.count('row') == 3


def test_modelformset_layout():
    CrispyModelFormSet = modelformset_factory(CrispyTestModel, form=TestForm4, extra=3)
    formset = CrispyModelFormSet(queryset=CrispyTestModel.objects.none())
    helper = FormHelper()
    helper.layout = Layout(
        'email'
    )

    html = render_crispy_form(form=formset, helper=helper)
    assert html.count("id_form-0-id") == 1
    assert html.count("id_form-1-id") == 1
    assert html.count("id_form-2-id") == 1

    assert html.count(
        'id="id_form-TOTAL_FORMS" name="form-TOTAL_FORMS" type="hidden" value="3"'
    ) == 1
    assert html.count(
        'id="id_form-INITIAL_FORMS" name="form-INITIAL_FORMS" type="hidden" value="0"'
    ) == 1
    assert html.count(
        'id="id_form-MAX_NUM_FORMS" name="form-MAX_NUM_FORMS" type="hidden" value="1000"'
    ) == 1

    assert html.count('name="form-0-email"') == 1
    assert html.count('name="form-1-email"') == 1
    assert html.count('name="form-2-email"') == 1
    assert html.count('name="form-3-email"') == 0
    assert html.count('password') == 0


def test_i18n():
    template = get_template_from_string("""
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
    assert html.count('i18n legend') == 1


def test_l10n(settings):
    settings.USE_L10N = True
    settings.USE_THOUSAND_SEPARATOR = True

    form = TestForm5(data={'pk': 1000})
    html = render_crispy_form(form)

    # Make sure values are unlocalized
    assert 'value="1,000"' not in html

    # Make sure label values are NOT localized.
    # Dirty check, which relates on HTML structure
    label_text = '>1000'
    if settings.CRISPY_TEMPLATE_PACK == 'uni_form':
        label_text = '/> 1000<'
    elif settings.CRISPY_TEMPLATE_PACK == 'bootstrap4':
        label_text = '>\n            1000'
    assert html.count(label_text) == 2


def test_default_layout():
    test_form = TestForm2()
    assert test_form.helper.layout.fields == [
        'is_company', 'email', 'password1', 'password2',
        'first_name', 'last_name', 'datetime_field',
    ]


def test_default_layout_two():
    test_form = TestForm3()
    assert test_form.helper.layout.fields == ['email']


def test_modelform_layout_without_meta():
    test_form = TestForm4()
    test_form.helper = FormHelper()
    test_form.helper.layout = Layout('email')
    html = render_crispy_form(test_form)

    assert 'email' in html
    assert 'password' not in html


def test_specialspaceless_not_screwing_intended_spaces():
    # see issue #250
    test_form = TestForm()
    test_form.fields['email'].widget = forms.Textarea()
    test_form.helper = FormHelper()
    test_form.helper.layout = Layout(
        'email',
        HTML("<span>first span</span> <span>second span</span>")
    )
    html = render_crispy_form(test_form)
    assert '<span>first span</span> <span>second span</span>' in html


@only_uni_form
def test_layout_composition():
    form_helper = FormHelper()
    form_helper.add_layout(
        Layout(
            Layout(
                MultiField(
                    "Some company data",
                    'is_company',
                    'email',
                    css_id="multifield_info",
                ),
            ),
            Column(
                'first_name',
                # 'last_name', Missing a field on purpose
                css_id="column_name",
                css_class="columns",
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

    template = get_template_from_string("""
            {% load crispy_forms_tags %}
            {% crispy form form_helper %}
        """)
    c = Context({'form': TestForm(), 'form_helper': form_helper})
    html = template.render(c)

    assert 'multiField' in html
    assert 'formColumn' in html
    assert 'id="multifield_info"' in html
    assert 'id="column_name"' in html
    assert 'class="formColumn columns"' in html
    assert 'class="buttonHolder">' in html
    assert 'input type="submit"' in html
    assert 'name="Save"' in html
    assert 'id="custom-div"' in html
    assert 'class="customdivs"' in html
    assert 'last_name' not in html


@only_uni_form
def test_second_layout_multifield_column_buttonholder_submit_div():
    form_helper = FormHelper()
    form_helper.add_layout(
        Layout(
            MultiField(
                "Some company data",
                'is_company',
                'email',
                css_id="multifield_info",
                title="multifield_title",
                multifield_test="123"
            ),
            Column(
                'first_name',
                'last_name',
                css_id="column_name",
                css_class="columns",
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

    template = get_template_from_string("""
            {% load crispy_forms_tags %}
            {% crispy form form_helper %}
        """)
    c = Context({'form': TestForm(), 'form_helper': form_helper, 'value_var': "Save"})
    html = template.render(c)

    assert 'multiField' in html
    assert 'formColumn' in html
    assert 'id="multifield_info"' in html
    assert 'title="multifield_title"' in html
    assert 'multifield-test="123"' in html
    assert 'id="column_name"' in html
    assert 'class="formColumn columns"' in html
    assert 'class="buttonHolder">' in html
    assert 'input type="submit"' in html
    assert 'button white' in html
    assert 'data-id="test"' in html
    assert 'data-name="test"' in html
    assert 'name="save-the-world"' in html
    assert 'value="Save"' in html
    assert 'name="store"' in html
    assert 'value="Store results"' in html
    assert 'id="custom-div"' in html
    assert 'class="customdivs"' in html
    assert 'test-markup="123"' in html


@only_bootstrap
def test_keepcontext_context_manager(settings):
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
    context = {'form': form}

    response = render_to_response('crispy_render_template.html', context)

    if settings.CRISPY_TEMPLATE_PACK == 'bootstrap':
        assert response.content.count(b'checkbox inline') == 3
    elif settings.CRISPY_TEMPLATE_PACK in ['bootstrap3', 'bootstrap4']:
        assert response.content.count(b'checkbox-inline') == 3


@only_bootstrap3
def test_form_inline():
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
    assert html.count('class="form-inline"') == 1
    assert html.count('class="form-group"') == 3
    assert html.count('<label for="id_email" class="sr-only') == 1
    assert html.count('id="div_id_email" class="form-group"') == 1
    assert html.count('placeholder="email"') == 1
    assert html.count('</label> <input') == 3


@only_bootstrap4
def test_bootstrap4_form_inline():
    form = TestForm()
    form.helper = FormHelper()
    form.helper.form_class = 'form-inline'
    form.helper.field_template = 'bootstrap4/layout/inline_field.html'
    form.helper.layout = Layout(
        'email',
        'password1',
        'last_name',
    )

    html = render_crispy_form(form)
    assert html.count('class="form-inline"') == 1
    assert html.count('class="form-group"') == 3
    assert html.count('<label for="id_email" class="sr-only') == 1
    assert html.count('id="div_id_email" class="form-group"') == 1
    assert html.count('placeholder="email"') == 1
    assert html.count('</label> <input') == 3
