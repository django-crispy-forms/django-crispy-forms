import pytest

from django import forms
from django.forms.models import formset_factory, modelformset_factory
from django.middleware.csrf import _get_new_csrf_string
from django.shortcuts import render
from django.template import Context, Template
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from crispy_forms.bootstrap import Field, InlineCheckboxes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, ButtonHolder, Column, Div, Fieldset, Layout, MultiField, Row, Submit
from crispy_forms.utils import render_crispy_form

from .conftest import only_bootstrap, only_bootstrap3, only_bootstrap4, only_uni_form
from .forms import (
    AdvancedFileForm,
    CheckboxesSampleForm,
    CrispyEmptyChoiceTestModel,
    CrispyTestModel,
    FileForm,
    SampleForm,
    SampleForm2,
    SampleForm3,
    SampleForm4,
    SampleForm5,
    SampleForm6,
    SelectSampleForm,
)
from .utils import contains_partial, parse_expected, parse_form


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


def test_layout_fieldset_row_html_with_unicode_fieldnames(settings):
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

    if settings.CRISPY_TEMPLATE_PACK == "uni_form":
        assert 'class="formRow rows"' in html
    elif settings.CRISPY_TEMPLATE_PACK == "bootstrap4":
        assert 'class="form-row rows"' in html
    else:
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
    form_helper = FormHelper()
    form_helper.add_layout(
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
    del form_helper.layout.fields[0].fields[1]

    c = Context({"form": form, "form_helper": form_helper})
    html = template.render(c)
    assert "email" not in html


def test_column_has_css_classes(settings):
    template = Template(
        """
        {% load crispy_forms_tags %}
        {% crispy form form_helper %}
    """
    )

    form = SampleForm()
    form_helper = FormHelper()
    form_helper.add_layout(
        Layout(
            Fieldset(
                "Company Data",
                "is_company",
                "email",
                "password1",
                "password2",
                css_id="multifield_info",
            ),
            Column("first_name", "last_name"),
        )
    )

    c = Context({"form": form, "form_helper": form_helper})
    html = template.render(c)

    if settings.CRISPY_TEMPLATE_PACK == "uni_form":
        assert html.count("formColumn") == 1
        assert html.count("col") == 0
    elif settings.CRISPY_TEMPLATE_PACK == "bootstrap4":
        assert html.count("formColumn") == 0
        assert html.count("col-md") == 1


@only_bootstrap4
def test_bs4_column_css_classes(settings):
    template = Template(
        """
        {% load crispy_forms_tags %}
        {% crispy form form_helper %}
    """
    )

    form = SampleForm()
    form_helper = FormHelper()
    form_helper.add_layout(
        Layout(
            Column("first_name", "last_name"),
            Column("first_name", "last_name", css_class="col-sm"),
            Column("first_name", "last_name", css_class="mb-4"),
        )
    )

    c = Context({"form": form, "form_helper": form_helper})
    html = template.render(c)

    assert html.count("col-md") == 2
    assert html.count("col-sm") == 1


def test_formset_layout(settings):
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

    html = render_crispy_form(form=formset, helper=helper, context={"csrf_token": _get_new_csrf_string()})

    # Check formset fields
    assert contains_partial(html, '<input id="id_form-TOTAL_FORMS" name="form-TOTAL_FORMS" type="hidden" value="3"/>')
    assert contains_partial(
        html, '<input id="id_form-INITIAL_FORMS" name="form-INITIAL_FORMS" type="hidden" value="0"/>'
    )
    assert contains_partial(
        html, '<input id="id_form-MAX_NUM_FORMS" name="form-MAX_NUM_FORMS" type="hidden" value="1000"/>'
    )
    assert contains_partial(
        html, '<input id="id_form-MIN_NUM_FORMS" name="form-MIN_NUM_FORMS" type="hidden" value="0"/>'
    )
    assert html.count("hidden") == 5

    # Check form structure
    assert html.count("<form") == 1
    assert html.count("csrfmiddlewaretoken") == 1
    assert "formsets-that-rock" in html
    assert 'method="post"' in html
    assert 'id="thisFormsetRocks"' in html
    assert 'action="%s"' % reverse("simpleAction") in html

    # Check form layout
    assert "Item 1" in html
    assert "Item 2" in html
    assert "Item 3" in html
    assert html.count("Note for first form only") == 1
    if settings.CRISPY_TEMPLATE_PACK == "uni_form":
        assert html.count("formRow") == 3
    elif settings.CRISPY_TEMPLATE_PACK in ("bootstrap3", "bootstrap4"):
        assert html.count("row") == 3

    if settings.CRISPY_TEMPLATE_PACK == "bootstrap4":
        assert html.count("form-group") == 18


def test_modelformset_layout():
    CrispyModelFormSet = modelformset_factory(CrispyTestModel, form=SampleForm4, extra=3)
    formset = CrispyModelFormSet(queryset=CrispyTestModel.objects.none())
    helper = FormHelper()
    helper.layout = Layout("email")

    html = render_crispy_form(form=formset, helper=helper)

    assert html.count("id_form-0-id") == 1
    assert html.count("id_form-1-id") == 1
    assert html.count("id_form-2-id") == 1

    assert contains_partial(html, '<input id="id_form-TOTAL_FORMS" name="form-TOTAL_FORMS" type="hidden" value="3"/>')
    assert contains_partial(
        html, '<input id="id_form-INITIAL_FORMS" name="form-INITIAL_FORMS" type="hidden" value="0"/>'
    )
    assert contains_partial(
        html, '<input id="id_form-MAX_NUM_FORMS" name="form-MAX_NUM_FORMS" type="hidden" value="1000"/>'
    )

    assert html.count('name="form-0-email"') == 1
    assert html.count('name="form-1-email"') == 1
    assert html.count('name="form-2-email"') == 1
    assert html.count('name="form-3-email"') == 0
    assert html.count("password") == 0


def test_i18n():
    template = Template(
        """
        {% load crispy_forms_tags %}
        {% crispy form form.helper %}
    """
    )
    form = SampleForm()
    form_helper = FormHelper()
    form_helper.layout = Layout(
        HTML(_("i18n text")),
        Fieldset(
            _("i18n legend"),
            "first_name",
            "last_name",
        ),
    )
    form.helper = form_helper

    html = template.render(Context({"form": form}))
    assert html.count("i18n legend") == 1


def test_default_layout():
    test_form = SampleForm2()
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
    test_form.helper = FormHelper()
    test_form.helper.layout = Layout("email")
    html = render_crispy_form(test_form)

    assert "email" in html
    assert "password" not in html


def test_specialspaceless_not_screwing_intended_spaces():
    # see issue #250
    test_form = SampleForm()
    test_form.fields["email"].widget = forms.Textarea()
    test_form.helper = FormHelper()
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


@only_uni_form
def test_layout_composition():
    form_helper = FormHelper()
    form_helper.add_layout(
        Layout(
            Layout(
                MultiField(
                    "Some company data",
                    "is_company",
                    "email",
                    css_id="multifield_info",
                ),
            ),
            Column(
                "first_name",
                # 'last_name', Missing a field on purpose
                css_id="column_name",
                css_class="columns",
            ),
            ButtonHolder(
                Submit("Save", "Save", css_class="button white"),
            ),
            Div(
                "password1",
                "password2",
                css_id="custom-div",
                css_class="customdivs",
            ),
        )
    )

    template = Template(
        """
            {% load crispy_forms_tags %}
            {% crispy form form_helper %}
        """
    )
    c = Context({"form": SampleForm(), "form_helper": form_helper})
    html = template.render(c)

    assert "multiField" in html
    assert "formColumn" in html
    assert 'id="multifield_info"' in html
    assert 'id="column_name"' in html
    assert 'class="formColumn columns"' in html
    assert 'class="buttonHolder">' in html
    assert 'input type="submit"' in html
    assert 'name="Save"' in html
    assert 'id="custom-div"' in html
    assert 'class="customdivs"' in html
    assert "last_name" not in html


@only_uni_form
def test_second_layout_multifield_column_buttonholder_submit_div():
    form_helper = FormHelper()
    form_helper.add_layout(
        Layout(
            MultiField(
                "Some company data",
                "is_company",
                "email",
                css_id="multifield_info",
                title="multifield_title",
                multifield_test="123",
            ),
            Column(
                "first_name",
                "last_name",
                css_id="column_name",
                css_class="columns",
            ),
            ButtonHolder(
                Submit(
                    "Save the world", "{{ value_var }}", css_class="button white", data_id="test", data_name="test"
                ),
                Submit("store", "Store results"),
            ),
            Div("password1", "password2", css_id="custom-div", css_class="customdivs", test_markup="123"),
        )
    )

    template = Template(
        """
            {% load crispy_forms_tags %}
            {% crispy form form_helper %}
        """
    )
    c = Context({"form": SampleForm(), "form_helper": form_helper, "value_var": "Save"})
    html = template.render(c)

    assert "multiField" in html
    assert "formColumn" in html
    assert 'id="multifield_info"' in html
    assert 'title="multifield_title"' in html
    assert 'multifield-test="123"' in html
    assert 'id="column_name"' in html
    assert 'class="formColumn columns"' in html
    assert 'class="buttonHolder">' in html
    assert 'input type="submit"' in html
    assert "button white" in html
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
    form = CheckboxesSampleForm()
    form.helper = FormHelper()
    # We use here InlineCheckboxes as it updates context in an unsafe way
    form.helper.layout = Layout("checkboxes", InlineCheckboxes("alphacheckboxes"), "numeric_multiple_checkboxes")
    context = {"form": form}

    response = render(request=None, template_name="crispy_render_template.html", context=context)

    if settings.CRISPY_TEMPLATE_PACK == "bootstrap":
        assert response.content.count(b"checkbox inline") == 3
    elif settings.CRISPY_TEMPLATE_PACK == "bootstrap3":
        assert response.content.count(b"checkbox-inline") == 3
    elif settings.CRISPY_TEMPLATE_PACK == "bootstrap4":
        assert response.content.count(b"custom-control-inline") == 3
        assert response.content.count(b"custom-checkbox") > 0


@only_bootstrap4
def test_use_custom_control_is_used_in_checkboxes():
    form = CheckboxesSampleForm()
    form.helper = FormHelper()
    form.helper.layout = Layout(
        "checkboxes",
        InlineCheckboxes("alphacheckboxes"),
        "numeric_multiple_checkboxes",
    )
    # form.helper.use_custom_control take default value which is True
    assert parse_form(form) == parse_expected(
        "bootstrap4/test_layout/test_use_custom_control_is_used_in_checkboxes_true.html"
    )

    form.helper.use_custom_control = True
    assert parse_form(form) == parse_expected(
        "bootstrap4/test_layout/test_use_custom_control_is_used_in_checkboxes_true.html"
    )

    form.helper.use_custom_control = False
    assert parse_form(form) == parse_expected(
        "bootstrap4/test_layout/test_use_custom_control_is_used_in_checkboxes_false.html"
    )

    form = CheckboxesSampleForm({})
    form.helper = FormHelper()
    form.helper.layout = Layout(
        "checkboxes",
        InlineCheckboxes("alphacheckboxes"),
        "numeric_multiple_checkboxes",
    )
    assert parse_form(form) == parse_expected(
        "bootstrap4/test_layout/test_use_custom_control_is_used_in_checkboxes_true_failing.html"
    )


@only_bootstrap4
def test_use_custom_control_is_used_in_radio():
    form = SampleForm5()
    form.helper = FormHelper()
    form.helper.layout = Layout(
        "radio_select",
    )
    # form.helper.use_custom_control take default value which is True
    assert parse_form(form) == parse_expected(
        "bootstrap4/test_layout/test_use_custom_control_is_used_in_radio_true.html"
    )

    form.helper.use_custom_control = True
    assert parse_form(form) == parse_expected(
        "bootstrap4/test_layout/test_use_custom_control_is_used_in_radio_true.html"
    )

    form.helper.use_custom_control = False
    assert parse_form(form) == parse_expected(
        "bootstrap4/test_layout/test_use_custom_control_is_used_in_radio_false.html"
    )

    form = SampleForm5({})
    form.helper = FormHelper()
    form.helper.layout = Layout(
        "radio_select",
    )
    assert parse_form(form) == parse_expected(
        "bootstrap4/test_layout/test_use_custom_control_is_used_in_radio_true_failing.html"
    )


@only_bootstrap4
@pytest.mark.parametrize(
    "use_custom_control, expected_html",
    [
        (True, "bootstrap4/test_layout/test_use_custom_control_in_select_true.html"),
        (False, "bootstrap4/test_layout/test_use_custom_control_in_select_false.html"),
    ],
)
def test_use_custom_control_in_select(use_custom_control, expected_html):
    form = SelectSampleForm()

    form.helper = FormHelper()
    form.helper.template_pack = "bootstrap4"
    form.helper.layout = Layout("select")
    form.helper.use_custom_control = use_custom_control

    assert parse_form(form) == parse_expected(expected_html)


@only_bootstrap3
def test_form_inline():
    form = SampleForm()
    form.helper = FormHelper()
    form.helper.form_class = "form-inline"
    form.helper.field_template = "bootstrap3/layout/inline_field.html"
    form.helper.layout = Layout(
        "email",
        "password1",
        "last_name",
    )

    html = render_crispy_form(form)
    assert html.count('class="form-inline"') == 1
    assert html.count('class="form-group"') == 3
    assert html.count('<label for="id_email" class="sr-only') == 1
    assert html.count('id="div_id_email" class="form-group"') == 1
    assert html.count('placeholder="email"') == 1
    assert html.count("</label> <input") == 3


@only_bootstrap4
def test_bootstrap4_form_inline():
    form = SampleForm()
    form.helper = FormHelper()
    form.helper.form_class = "form-inline"
    form.helper.field_template = "bootstrap4/layout/inline_field.html"
    form.helper.layout = Layout("email", "password1", "last_name")

    html = render_crispy_form(form)
    assert html.count('class="form-inline"') == 1
    assert html.count('class="input-group"') == 3
    assert html.count('<label for="id_email" class="sr-only') == 1
    assert html.count('id="div_id_email" class="input-group"') == 1
    assert html.count('placeholder="email"') == 1
    assert html.count("</label> <input") == 3


def test_update_attributes_class():
    form = SampleForm()
    form.helper = FormHelper()
    form.helper.layout = Layout("email", Field("password1"), "password2")
    form.helper["password1"].update_attributes(css_class="hello")
    html = render_crispy_form(form)
    assert html.count(' class="hello textinput') == 1
    form.helper = FormHelper()
    form.helper.layout = Layout(
        "email",
        Field("password1", css_class="hello"),
        "password2",
    )
    form.helper["password1"].update_attributes(css_class="hello2")
    html = render_crispy_form(form)
    assert html.count(' class="hello hello2 textinput') == 1


@only_bootstrap4
def test_file_field():
    form = FileForm()
    form.helper = FormHelper()
    form.helper.layout = Layout("clearable_file")
    assert parse_form(form) == parse_expected("bootstrap4/test_layout/test_file_field_clearable_custom_control.html")

    form.helper.use_custom_control = False
    assert parse_form(form) == parse_expected("bootstrap4/test_layout/test_file_field_clearable.html")

    form.helper.use_custom_control = True
    form.helper.layout = Layout("file_field")
    assert parse_form(form) == parse_expected("bootstrap4/test_layout/test_file_field_custom_control.html")

    form.helper.use_custom_control = False
    assert parse_form(form) == parse_expected("bootstrap4/test_layout/test_file_field_default.html")


@only_bootstrap4
def test_file_field_with_custom_class():
    form = AdvancedFileForm()
    form.helper = FormHelper()
    form.helper.layout = Layout("clearable_file")
    assert parse_form(form) == parse_expected(
        "bootstrap4/test_layout/test_file_field_with_custom_class_clearable.html"
    )

    form.helper.layout = Layout("file_field")
    assert parse_form(form) == parse_expected("bootstrap4/test_layout/test_file_field_with_custom_class.html")


@only_bootstrap4
def test_form_control_size():
    "CSS classes form-control and form-control-lg are both required"
    form = SampleForm()
    form.helper = FormHelper()
    form.helper.layout = Layout(Field("first_name", css_class="form-control-lg"))
    assert parse_form(form) == parse_expected("bootstrap4/test_layout/test_form_control_size.html")
