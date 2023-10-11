import django
import pytest
from django import forms
from django.forms.models import formset_factory, modelformset_factory
from django.shortcuts import render
from django.template import Context, Template
from django.test.html import parse_html
from django.test.utils import override_settings
from django.utils.translation import gettext_lazy as _

from crispy_forms.bootstrap import Field, InlineCheckboxes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Fieldset, Layout, Row
from crispy_forms.utils import render_crispy_form

from .forms import (
    CheckboxesSampleForm,
    CrispyEmptyChoiceTestModel,
    CrispyTestModel,
    SampleForm,
    SampleForm3,
    SampleForm4,
    SampleForm6,
)
from .test_settings import TEMPLATE_DIRS
from .utils import parse_expected, parse_form


def test_invalid_unicode_characters(settings):
    # Adds a BooleanField that uses non valid unicode characters "ñ"
    form_helper = FormHelper()
    form_helper.add_layout(Layout("españa"))

    template = Template(
        """
        {% load crispy_forms_tags %}
        {% crispy form form_helper %}
    """
    )
    c = Context({"form": SampleForm(), "form_helper": form_helper})
    settings.CRISPY_FAIL_SILENTLY = False
    with pytest.raises(Exception):
        template.render(c)


def test_unicode_form_field():
    class UnicodeForm(forms.Form):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["contraseña"] = forms.CharField()

        helper = FormHelper()
        helper.layout = Layout("contraseña")

    html = render_crispy_form(UnicodeForm())
    assert 'id="id_contraseña"' in html


def test_meta_extra_fields_with_missing_fields():
    class FormWithMeta(SampleForm):
        class Meta:
            fields = ("email", "first_name", "last_name")

    form = FormWithMeta()
    # We remove email field on the go
    del form.fields["email"]

    form_helper = FormHelper()
    form_helper.layout = Layout("first_name")

    template = Template(
        """
        {% load crispy_forms_tags %}
        {% crispy form form_helper %}
    """
    )
    c = Context({"form": form, "form_helper": form_helper})
    html = template.render(c)
    assert "email" not in html


def test_layout_unresolved_field(settings):
    form_helper = FormHelper()
    form_helper.add_layout(Layout("typo"))

    template = Template(
        """
        {% load crispy_forms_tags %}
        {% crispy form form_helper %}
    """
    )
    c = Context({"form": SampleForm(), "form_helper": form_helper})
    settings.CRISPY_FAIL_SILENTLY = False
    with pytest.raises(Exception):
        template.render(c)


def test_double_rendered_field(settings):
    form_helper = FormHelper()
    form_helper.add_layout(Layout("is_company", "is_company"))

    template = Template(
        """
        {% load crispy_forms_tags %}
        {% crispy form form_helper %}
    """
    )
    c = Context({"form": SampleForm(), "form_helper": form_helper})
    settings.CRISPY_FAIL_SILENTLY = False
    with pytest.raises(Exception):
        template.render(c)


def test_context_pollution():
    class ExampleForm(forms.Form):
        comment = forms.CharField()

    form = ExampleForm()
    form2 = SampleForm()

    template = Template(
        """
        {% load crispy_forms_tags %}
        {{ form.as_ul }}
        {% crispy form2 %}
        {{ form.as_ul }}
    """
    )
    c = Context({"form": form, "form2": form2})
    html = template.render(c)

    assert html.count('name="comment"') == 2
    assert html.count('name="is_company"') == 1


def test_layout_fieldset_row_html_with_unicode_fieldnames():
    form_helper = FormHelper()
    form_helper.add_layout(
        Layout(
            Fieldset(
                "Company Data",
                "is_company",
                css_id="fieldset_company_data",
                css_class="fieldsets",
                title="fieldset_title",
                test_fieldset="123",
            ),
            Fieldset(
                "User Data",
                "email",
                Row(
                    "password1",
                    "password2",
                    css_id="row_passwords",
                    css_class="rows",
                ),
                HTML('<a href="#" id="testLink">test link</a>'),
                HTML(
                    """
                    {% if flag %}{{ message }}{% endif %}
                """
                ),
                "first_name",
                "last_name",
            ),
        )
    )

    template = Template(
        """
        {% load crispy_forms_tags %}
        {% crispy form form_helper %}
    """
    )
    c = Context({"form": SampleForm(), "form_helper": form_helper, "flag": True, "message": "Hello!"})
    html = template.render(c)

    assert 'id="fieldset_company_data"' in html
    assert 'class="fieldsets' in html
    assert 'title="fieldset_title"' in html
    assert 'test-fieldset="123"' in html
    assert 'id="row_passwords"' in html
    assert html.count("<label") == 6
    assert 'class="row rows"' in html
    assert "Hello!" in html
    assert "testLink" in html


def test_change_layout_dynamically_delete_field():
    template = Template(
        """
        {% load crispy_forms_tags %}
        {% crispy form form_helper %}
    """
    )

    form = SampleForm()
    form.helper.add_layout(
        Layout(
            Fieldset(
                "Company Data",
                "is_company",
                "email",
                "password1",
                "password2",
                css_id="multifield_info",
            ),
            Column(
                "first_name",
                "last_name",
                css_id="column_name",
            ),
        )
    )

    # We remove email field on the go
    # Layout needs to be adapted for the new form fields
    del form.fields["email"]
    del form.helper.layout.fields[0].fields[1]

    c = Context({"form": form, "form_helper": form.helper})
    html = template.render(c)
    assert "email" not in html


def test_formset_layout():
    SampleFormSet = formset_factory(SampleForm, extra=3)
    formset = SampleFormSet()
    helper = FormHelper()
    helper.form_id = "thisFormsetRocks"
    helper.form_class = "formsets-that-rock"
    helper.form_method = "POST"
    helper.form_action = "simpleAction"
    helper.layout = Layout(
        Fieldset(
            "Item {{ forloop.counter }}",
            "is_company",
            "email",
        ),
        HTML("{% if forloop.first %}Note for first form only{% endif %}"),
        Row("password1", "password2"),
        Fieldset("", "first_name", "last_name"),
    )

    html = render_crispy_form(form=formset, helper=helper, context={"csrf_token": "aTestToken"})
    if django.VERSION < (5, 0):
        result = "test_formset_layout lt50.html"
    else:
        result = "test_formset_layout.html"
    assert parse_expected(result) == parse_html(html)


def test_modelformset_layout():
    CrispyModelFormSet = modelformset_factory(CrispyTestModel, form=SampleForm4, extra=3)
    formset = CrispyModelFormSet(queryset=CrispyTestModel.objects.none())
    formset.helper = FormHelper()
    formset.helper.layout = Layout("email")
    assert parse_expected("test_modelformset_layout.html") == parse_form(formset)


def test_i18n():
    template = Template(
        """
        {% load crispy_forms_tags %}
        {% crispy form form.helper %}
    """
    )
    form = SampleForm()
    form.helper.layout = Layout(
        HTML(_("i18n text")),
        Fieldset(
            _("i18n legend"),
            "first_name",
            "last_name",
        ),
    )
    html = template.render(Context({"form": form}))
    assert html.count("i18n legend") == 1


def test_default_layout():
    test_form = SampleForm()
    assert test_form.helper.layout.fields == [
        "is_company",
        "email",
        "password1",
        "password2",
        "first_name",
        "last_name",
        "datetime_field",
    ]


def test_default_layout_two():
    test_form = SampleForm3()
    assert test_form.helper.layout.fields == ["email"]


def test_modelform_layout_without_meta():
    test_form = SampleForm4()
    test_form.helper.layout = Layout("email")
    html = render_crispy_form(test_form)

    assert "email" in html
    assert "password" not in html


def test_specialspaceless_not_screwing_intended_spaces():
    # see issue #250
    test_form = SampleForm()
    test_form.fields["email"].widget = forms.Textarea()
    test_form.helper.layout = Layout("email", HTML("<span>first span</span> <span>second span</span>"))
    html = render_crispy_form(test_form)
    assert "<span>first span</span> <span>second span</span>" in html


def test_choice_with_none_is_selected():
    # see issue #701
    model_instance = CrispyEmptyChoiceTestModel()
    model_instance.fruit = None
    test_form = SampleForm6(instance=model_instance)
    html = render_crispy_form(test_form)
    assert "checked" in html


@override_settings(
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": TEMPLATE_DIRS,
            "OPTIONS": {
                "loaders": [
                    "django.template.loaders.filesystem.Loader",
                    "django.template.loaders.app_directories.Loader",
                ],
            },
        }
    ]
)
def test_keepcontext_context_manager():
    # Test case for issue #180
    # Apparently it only manifest when using render_to_response this exact way
    form = CheckboxesSampleForm()
    # We use here InlineCheckboxes as it updates context in an unsafe way
    form.helper.layout = Layout("checkboxes", InlineCheckboxes("alphacheckboxes"), "numeric_multiple_checkboxes")
    context = {"form": form}

    response = render(request=None, template_name="crispy_render_template.html", context=context)

    assert response.content.count(b"checkbox-inline") == 3


def test_update_attributes_class():
    form = SampleForm()
    form.helper.layout = Layout("email", Field("password1"), "password2")
    form.helper["password1"].update_attributes(css_class="hello")
    html = render_crispy_form(form)
    assert html.count(' class="hello') == 1
    form.helper.layout = Layout(
        "email",
        Field("password1", css_class="hello"),
        "password2",
    )
    form.helper["password1"].update_attributes(css_class="hello2")
    html = render_crispy_form(form)
    assert html.count(' class="hello hello2') == 1
