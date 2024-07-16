from django import forms
from django.template import Context, Template
from django.utils.translation import activate, deactivate
from django.utils.translation import gettext as _

from crispy_forms.bootstrap import (
    Accordion,
    AccordionGroup,
    Alert,
    AppendedText,
    Container,
    InlineCheckboxes,
    InlineRadios,
    PrependedAppendedText,
    PrependedText,
    Tab,
    TabHolder,
)
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Field, Fieldset, Layout, MultiWidgetField
from crispy_forms.utils import render_crispy_form

from .forms import (
    CheckboxesSampleForm,
    CustomCheckboxSelectMultiple,
    CustomRadioSelect,
    SampleForm,
    SampleFormCustomWidgets,
)


def test_field_with_custom_template():
    test_form = SampleForm()
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


def test_field_wrapper_class():
    form = SampleForm()
    form.helper.layout = Layout(Field("email", wrapper_class="testing"))

    html = render_crispy_form(form)
    assert html.count('class="form-group testing"') == 1


def test_html_with_carriage_returns():
    test_form = SampleForm()
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
    assert html.count("\n") == 27


def test_i18n():
    activate("es")
    form = SampleForm()
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


def test_passthrough_context():
    """
    Test to ensure that context is passed through implicitly from outside of
    the crispy form into the crispy form templates.
    """
    form = SampleForm()
    form.helper.layout = Layout(
        Fieldset("", template="custom_fieldset_template_with_context.html"),
    )

    c = {"fieldset_context_var": "fieldset_context_value"}

    html = render_crispy_form(form, helper=form.helper, context=c)
    assert "Got context var: fieldset_context_value" in html


class TestBootstrapLayoutObjects:
    def test_custom_django_widget(self):
        # Make sure an inherited RadioSelect gets rendered as it
        form = SampleFormCustomWidgets()
        assert isinstance(form.fields["inline_radios"].widget, CustomRadioSelect)
        form.helper.layout = Layout("inline_radios")

        html = render_crispy_form(form)
        assert 'class="radio"' in html

        # Make sure an inherited CheckboxSelectMultiple gets rendered as it
        assert isinstance(form.fields["checkboxes"].widget, CustomCheckboxSelectMultiple)
        form.helper.layout = Layout("checkboxes")
        html = render_crispy_form(form)
        assert 'class="checkbox"' in html

    def test_inline_radios(self):
        test_form = CheckboxesSampleForm()
        test_form.helper.layout = Layout(InlineRadios("inline_radios"))
        html = render_crispy_form(test_form)
        assert html.count('radio-inline"') == 2

    def test_accordion_and_accordiongroup(self):
        test_form = SampleForm()
        test_form.helper.layout = Layout(
            Accordion(
                AccordionGroup("one", "first_name"),
                AccordionGroup("two", "password1", "password2"),
            )
        )
        html = render_crispy_form(test_form)

        assert html.count('<div class="panel panel-default"') == 2
        assert html.count('<div class="panel-group"') == 1
        assert html.count('<div class="panel-heading">') == 2
        assert html.count('<div id="one"') == 1
        assert html.count('<div id="two"') == 1
        assert html.count('name="first_name"') == 1
        assert html.count('name="password1"') == 1
        assert html.count('name="password2"') == 1

    def test_accordion_active_false_not_rendered(self):
        test_form = SampleForm()
        test_form.helper.layout = Layout(
            Accordion(
                AccordionGroup("one", "first_name"),
                # there is no ``active`` kwarg here.
            )
        )

        # The first time, there should be one of them there.
        html = render_crispy_form(test_form)

        accordion_class = "panel-collapse collapse in"

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
        test_form.helper.layout = Layout(Alert(content="Testing..."))
        html = render_crispy_form(test_form)

        assert html.count('<div class="alert"') == 1
        assert html.count('<button type="button" class="close"') == 1
        assert html.count("Testing...") == 1

    def test_alert_block(self):
        test_form = SampleForm()
        test_form.helper.layout = Layout(Alert(content="Testing...", block=True))
        html = render_crispy_form(test_form)

        assert html.count('<div class="alert alert-block"') == 1
        assert html.count("Testing...") == 1

    def test_tab_and_tab_holder(self):
        test_form = SampleForm()
        test_form.helper.layout = Layout(
            TabHolder(
                Tab("one", "first_name", css_id="custom-name", css_class="first-tab-class active"),
                Tab("two", "password1", "password2"),
            )
        )
        html = render_crispy_form(test_form)

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

    def test_hidden_fields(self):
        form = SampleForm()
        # All fields hidden
        for field in form.fields:
            form.fields[field].widget = forms.HiddenInput()

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

    def test_multiplecheckboxes(self):
        test_form = CheckboxesSampleForm()
        html = render_crispy_form(test_form)

        assert html.count("checked") == 6

        test_form.helper[1].wrap(InlineCheckboxes, inline=True)
        html = render_crispy_form(test_form)

        assert html.count('inline="True"') == 4
        assert html.count('checkbox-inline"') == 3

    def test_multiple_checkboxes_unique_ids(self):
        test_form = CheckboxesSampleForm()
        html = render_crispy_form(test_form)

        expected_ids = [
            "checkboxes_0",
            "checkboxes_1",
            "checkboxes_2",
            "alphacheckboxes_0",
            "alphacheckboxes_1",
            "alphacheckboxes_2",
            "numeric_multiple_checkboxes_0",
            "numeric_multiple_checkboxes_1",
            "numeric_multiple_checkboxes_2",
        ]
        for id_suffix in expected_ids:
            expected_str = f'id="id_{id_suffix}"'
            assert html.count(expected_str) == 1

    def test_non_ascii_chars_in_container_name(self):
        """
        Test if non-ASCII characters are saved as css_id property.
        """
        name = "テスト"
        test_container = Container(name, "val1", "val2")
        assert test_container.css_id == name
