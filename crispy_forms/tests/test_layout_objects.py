from django import forms
from django.template import Context, Template
from django.test.html import parse_html
from django.utils.translation import activate, deactivate
from django.utils.translation import gettext as _

from crispy_forms.bootstrap import (
    Accordion,
    AccordionGroup,
    Alert,
    AppendedText,
    FieldWithButtons,
    InlineCheckboxes,
    InlineRadios,
    PrependedAppendedText,
    PrependedText,
    StrictButton,
    Tab,
    TabHolder,
)
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Field, Layout, MultiWidgetField
from crispy_forms.tests.utils import contains_partial
from crispy_forms.utils import render_crispy_form

from .conftest import only_bootstrap
from .forms import CheckboxesSampleForm, SampleForm


def test_field_with_custom_template():
    test_form = SampleForm()
    test_form.helper = FormHelper()
    test_form.helper.layout = Layout(Field("email", template="custom_field_template.html"))

    html = render_crispy_form(test_form)
    assert "<h1>Special custom field</h1>" in html


def test_multiwidget_field():
    template = Template(
        """
        {% load crispy_forms_tags %}
        {% crispy form %}
    """
    )

    test_form = SampleForm()
    test_form.helper = FormHelper()
    test_form.helper.layout = Layout(
        MultiWidgetField(
            "datetime_field",
            attrs=({"rel": "test_dateinput"}, {"rel": "test_timeinput", "style": "width: 30px;", "type": "hidden"}),
        )
    )

    c = Context({"form": test_form})

    html = template.render(c)

    assert html.count('class="dateinput') == 1
    assert html.count('rel="test_dateinput"') == 1
    assert html.count('rel="test_timeinput"') == 2
    assert html.count('style="width: 30px;"') == 2
    assert html.count('type="hidden"') == 2


def test_field_type_hidden():
    template = Template(
        """
        {% load crispy_forms_tags %}
        {% crispy test_form %}
    """
    )

    test_form = SampleForm()
    test_form.helper = FormHelper()
    test_form.helper.layout = Layout(
        Field("email", type="hidden", data_test=12),
        Field("datetime_field"),
    )

    c = Context({"test_form": test_form})
    html = template.render(c)

    # Check form parameters
    assert html.count('data-test="12"') == 1
    assert html.count('name="email"') == 1
    assert html.count('class="dateinput') == 1
    assert html.count('class="timeinput') == 1


def test_field_wrapper_class(settings):
    form = SampleForm()
    form.helper = FormHelper()
    form.helper.layout = Layout(Field("email", wrapper_class="testing"))

    html = render_crispy_form(form)
    if settings.CRISPY_TEMPLATE_PACK == "bootstrap":
        assert html.count('class="control-group testing"') == 1
    elif settings.CRISPY_TEMPLATE_PACK in ("bootstrap3", "bootstrap4"):
        assert html.count('class="form-group testing"') == 1


def test_html_with_carriage_returns(settings):
    test_form = SampleForm()
    test_form.helper = FormHelper()
    test_form.helper.layout = Layout(
        HTML(
            """
            if (a==b){
                // some comment
                a+1;
                foo();
            }
        """
        )
    )
    html = render_crispy_form(test_form)

    if settings.CRISPY_TEMPLATE_PACK == "uni_form":
        assert html.count("\n") == 23
    elif settings.CRISPY_TEMPLATE_PACK == "bootstrap":
        assert html.count("\n") == 25
    else:
        assert html.count("\n") == 27


def test_i18n():
    activate("es")
    form = SampleForm()
    form.helper = FormHelper()
    form.helper.layout = Layout(HTML(_("Enter a valid value.")))
    html = render_crispy_form(form)
    assert "Introduzca un valor válido" in html

    deactivate()


def test_remove_labels():
    form = SampleForm()
    # remove boolean field as label is still printed in boostrap
    del form.fields["is_company"]

    for fields in form:
        fields.label = False

    html = render_crispy_form(form)

    assert "<label" not in html


@only_bootstrap
class TestBootstrapLayoutObjects:
    def test_custom_django_widget(self, settings):
        class CustomRadioSelect(forms.RadioSelect):
            pass

        class CustomCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
            pass

        # Make sure an inherited RadioSelect gets rendered as it
        form = CheckboxesSampleForm()
        form.fields["inline_radios"].widget = CustomRadioSelect()
        form.helper = FormHelper()
        form.helper.layout = Layout("inline_radios")

        html = render_crispy_form(form)
        if settings.CRISPY_TEMPLATE_PACK == "bootstrap4":
            assert 'class="custom-control-input"' in html
        else:
            assert 'class="radio"' in html

        # Make sure an inherited CheckboxSelectMultiple gets rendered as it
        form.fields["checkboxes"].widget = CustomCheckboxSelectMultiple()
        form.helper.layout = Layout("checkboxes")
        html = render_crispy_form(form)
        if settings.CRISPY_TEMPLATE_PACK == "bootstrap4":
            assert 'class="custom-control-input"' in html
        else:
            assert 'class="checkbox"' in html

    def test_prepended_appended_text(self, settings):
        test_form = SampleForm()
        test_form.helper = FormHelper()
        test_form.helper.layout = Layout(
            PrependedAppendedText("email", "@", "gmail.com"),
            AppendedText("password1", "#"),
            PrependedText("password2", "$"),
        )
        html = render_crispy_form(test_form)
        dom = parse_html(html)

        # Check form parameters
        if settings.CRISPY_TEMPLATE_PACK == "bootstrap":
            assert dom.count(parse_html('<span class="add-on">@</span>')) == 1
            assert dom.count(parse_html('<span class="add-on">gmail.com</span>')) == 1
            assert dom.count(parse_html('<span class="add-on">#</span>')) == 1
            assert dom.count(parse_html('<span class="add-on">$</span>')) == 1

        if settings.CRISPY_TEMPLATE_PACK == "bootstrap3":
            assert html.count('<span class="input-group-addon">@</span>') == 1
            assert html.count('<span class="input-group-addon">gmail.com</span>') == 1
            assert html.count('<span class="input-group-addon">#</span>') == 1
            assert html.count('<span class="input-group-addon">$</span>') == 1
            test_form.helper.layout = Layout(
                PrependedAppendedText("email", "@", "gmail.com", css_class="input-lg"),
            )
            html = render_crispy_form(test_form)

            assert 'class="input-lg' in html
            assert contains_partial(html, '<span class="input-group-addon input-lg"/>')

        if settings.CRISPY_TEMPLATE_PACK == "bootstrap4":
            assert html.count('<span class="input-group-text">@</span>') == 1
            assert html.count('<span class="input-group-text">gmail.com</span>') == 1
            assert html.count('<span class="input-group-text">#</span>') == 1
            assert html.count('<span class="input-group-text">$</span>') == 1
            test_form.helper.layout = Layout(
                PrependedAppendedText("email", "@", "gmail.com", css_class="form-control-lg")
            )
            html = render_crispy_form(test_form)

            assert 'class="form-control-lg' in html
            assert contains_partial(html, '<span class="input-group-text"/>')

    def test_inline_radios(self, settings):
        test_form = CheckboxesSampleForm()
        test_form.helper = FormHelper()
        test_form.helper.layout = Layout(InlineRadios("inline_radios"))
        html = render_crispy_form(test_form)

        if settings.CRISPY_TEMPLATE_PACK == "bootstrap":
            assert html.count('radio inline"') == 2
        elif settings.CRISPY_TEMPLATE_PACK == "bootstrap3":
            assert html.count('radio-inline"') == 2
        elif settings.CRISPY_TEMPLATE_PACK == "bootstrap4":
            assert html.count('custom-control-inline"') == 2

    def test_accordion_and_accordiongroup(self, settings):
        test_form = SampleForm()
        test_form.helper = FormHelper()
        test_form.helper.layout = Layout(
            Accordion(
                AccordionGroup("one", "first_name"),
                AccordionGroup("two", "password1", "password2"),
            )
        )
        html = render_crispy_form(test_form)

        if settings.CRISPY_TEMPLATE_PACK == "bootstrap":
            assert html.count('<div class="accordion"') == 1
            assert html.count('<div class="accordion-group">') == 2
            assert html.count('<div class="accordion-heading">') == 2
        elif settings.CRISPY_TEMPLATE_PACK == "bootstrap3":
            assert html.count('<div class="panel panel-default"') == 2
            assert html.count('<div class="panel-group"') == 1
            assert html.count('<div class="panel-heading">') == 2
        elif settings.CRISPY_TEMPLATE_PACK == "bootstrap4":
            assert html.count('<div id="accordion"') == 1
            assert html.count('<div class="card mb-2"') == 2
            assert html.count('<div class="card-header"') == 2

        assert html.count('<div id="one"') == 1
        assert html.count('<div id="two"') == 1
        assert html.count('name="first_name"') == 1
        assert html.count('name="password1"') == 1
        assert html.count('name="password2"') == 1

    def test_accordion_active_false_not_rendered(self, settings):
        test_form = SampleForm()
        test_form.helper = FormHelper()
        test_form.helper.layout = Layout(
            Accordion(
                AccordionGroup("one", "first_name"),
                # there is no ``active`` kwarg here.
            )
        )

        # The first time, there should be one of them there.
        html = render_crispy_form(test_form)

        if settings.CRISPY_TEMPLATE_PACK == "bootstrap":
            accordion_class = "accordion-body collapse in"
        elif settings.CRISPY_TEMPLATE_PACK == "bootstrap3":
            accordion_class = "panel-collapse collapse in"
        elif settings.CRISPY_TEMPLATE_PACK == "bootstrap4":
            accordion_class = "collapse show"

        assert html.count('<div id="one" class="%s"' % accordion_class) == 1

        test_form.helper.layout = Layout(
            Accordion(
                AccordionGroup("one", "first_name", active=False),
            )  # now ``active`` manually set as False
        )

        # This time, it shouldn't be there at all.
        html = render_crispy_form(test_form)
        assert html.count('<div id="one" class="%s collapse in"' % accordion_class) == 0

    def test_alert(self):
        test_form = SampleForm()
        test_form.helper = FormHelper()
        test_form.helper.layout = Layout(Alert(content="Testing..."))
        html = render_crispy_form(test_form)

        assert html.count('<div class="alert"') == 1
        assert html.count('<button type="button" class="close"') == 1
        assert html.count("Testing...") == 1

    def test_alert_block(self):
        test_form = SampleForm()
        test_form.helper = FormHelper()
        test_form.helper.layout = Layout(Alert(content="Testing...", block=True))
        html = render_crispy_form(test_form)

        assert html.count('<div class="alert alert-block"') == 1
        assert html.count("Testing...") == 1

    def test_tab_and_tab_holder(self, settings):
        test_form = SampleForm()
        test_form.helper = FormHelper()
        test_form.helper.layout = Layout(
            TabHolder(
                Tab("one", "first_name", css_id="custom-name", css_class="first-tab-class active"),
                Tab("two", "password1", "password2"),
            )
        )
        html = render_crispy_form(test_form)

        if settings.CRISPY_TEMPLATE_PACK == "bootstrap4":
            assert (
                html.count(
                    '<ul class="nav nav-tabs"> <li class="nav-item">'
                    '<a class="nav-link active" href="#custom-name" data-toggle="tab">One</a></li>'
                )
                == 1
            )
            assert html.count("tab-pane") == 2
        else:
            assert (
                html.count(
                    '<ul class="nav nav-tabs"> <li class="tab-pane active">'
                    '<a href="#custom-name" data-toggle="tab">One</a></li>'
                )
                == 1
            )
            assert html.count('<li class="tab-pane') == 2
            assert html.count("tab-pane") == 4

        assert html.count('class="tab-pane first-tab-class active"') == 1

        assert html.count('<div id="custom-name"') == 1
        assert html.count('<div id="two"') == 1
        assert html.count('name="first_name"') == 1
        assert html.count('name="password1"') == 1
        assert html.count('name="password2"') == 1

    def test_tab_helper_reuse(self):
        # this is a proper form, according to the docs.
        # note that the helper is a class property here,
        # shared between all instances
        class SampleForm(forms.Form):
            val1 = forms.CharField(required=False)
            val2 = forms.CharField(required=True)
            helper = FormHelper()
            helper.layout = Layout(
                TabHolder(
                    Tab("one", "val1"),
                    Tab("two", "val2"),
                )
            )

        # first render of form => everything is fine
        test_form = SampleForm()
        html = render_crispy_form(test_form)

        # second render of form => first tab should be active,
        # but not duplicate class
        test_form = SampleForm()
        html = render_crispy_form(test_form)
        assert html.count('class="nav-item active active"') == 0

        # render a new form, now with errors
        test_form = SampleForm(data={"val1": "foo"})
        html = render_crispy_form(test_form)
        tab_class = "tab-pane"
        # if settings.CRISPY_TEMPLATE_PACK == 'bootstrap4':
        # tab_class = 'nav-link'
        # else:
        # tab_class = 'tab-pane'
        # tab 1 should not be active
        assert html.count('<div id="one" \n    class="{} active'.format(tab_class)) == 0
        # tab 2 should be active
        assert html.count('<div id="two" \n    class="{} active'.format(tab_class)) == 1

    def test_radio_attrs(self):
        form = CheckboxesSampleForm()
        form.fields["inline_radios"].widget.attrs = {"class": "first"}
        form.fields["checkboxes"].widget.attrs = {"class": "second"}
        html = render_crispy_form(form)
        assert 'class="first"' in html
        assert 'class="second"' in html

    def test_field_with_buttons(self, settings):
        form = SampleForm()
        form.helper = FormHelper()
        form.helper.layout = Layout(
            FieldWithButtons(
                Field("password1", css_class="span4"),
                StrictButton("Go!", css_id="go-button"),
                StrictButton("No!", css_class="extra"),
                StrictButton("Test", type="submit", name="whatever", value="something"),
                css_class="extra",
                autocomplete="off",
            )
        )
        html = render_crispy_form(form)

        form_group_class = "control-group"
        if settings.CRISPY_TEMPLATE_PACK in ("bootstrap3", "bootstrap4"):
            form_group_class = "form-group"

        assert html.count('class="%s extra"' % form_group_class) == 1
        assert html.count('autocomplete="off"') == 1
        assert html.count('class="span4') == 1
        assert html.count('id="go-button"') == 1
        assert html.count("Go!") == 1
        assert html.count("No!") == 1
        assert html.count('class="btn"') == 2
        assert html.count('class="btn extra"') == 1
        assert html.count('type="submit"') == 1
        assert html.count('name="whatever"') == 1
        assert html.count('value="something"') == 1

        if settings.CRISPY_TEMPLATE_PACK == "bootstrap":
            assert html.count('class="input-append"') == 1
        elif settings.CRISPY_TEMPLATE_PACK == "bootstrap3":
            assert html.count('class="input-group-btn') == 1
        elif settings.CRISPY_TEMPLATE_PACK == "bootstrap4":
            assert html.count('class="input-group-append') == 1

    def test_hidden_fields(self):
        form = SampleForm()
        # All fields hidden
        for field in form.fields:
            form.fields[field].widget = forms.HiddenInput()

        form.helper = FormHelper()
        form.helper.layout = Layout(
            AppendedText("password1", "foo"),
            PrependedText("password2", "bar"),
            PrependedAppendedText("email", "bar"),
            InlineCheckboxes("first_name"),
            InlineRadios("last_name"),
        )
        html = render_crispy_form(form)
        assert html.count("<input") == 5
        assert html.count('type="hidden"') == 5
        assert html.count("<label") == 0

    def test_multiplecheckboxes(self, settings):
        test_form = CheckboxesSampleForm()
        html = render_crispy_form(test_form)

        assert html.count('checked="checked"') == 6

        test_form.helper = FormHelper(test_form)
        test_form.helper[1].wrap(InlineCheckboxes, inline=True)
        html = render_crispy_form(test_form)

        if settings.CRISPY_TEMPLATE_PACK == "bootstrap":
            assert html.count('checkbox inline"') == 3
            assert html.count('inline"') == 3
        elif settings.CRISPY_TEMPLATE_PACK in ["bootstrap3", "bootstrap4"]:
            assert html.count('inline="True"') == 4
            if settings.CRISPY_TEMPLATE_PACK == "bootstrap3":
                assert html.count('checkbox-inline"') == 3
            elif settings.CRISPY_TEMPLATE_PACK == "bootstrap4":
                assert html.count('custom-control-inline"') == 3

    def test_multiple_checkboxes_unique_ids(self):
        test_form = CheckboxesSampleForm()
        html = render_crispy_form(test_form)

        expected_ids = [
            "checkboxes_1",
            "checkboxes_2",
            "checkboxes_3",
            "alphacheckboxes_1",
            "alphacheckboxes_2",
            "alphacheckboxes_3",
            "numeric_multiple_checkboxes_1",
            "numeric_multiple_checkboxes_2",
            "numeric_multiple_checkboxes_3",
        ]
        for id_suffix in expected_ids:
            expected_str = 'id="id_{id_suffix}"'.format(id_suffix=id_suffix)
            assert html.count(expected_str) == 1
