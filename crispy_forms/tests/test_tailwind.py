from crispy_forms.tailwind import CSSContainer
from django.template import Context, Template
from .forms import SampleForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from  .conftest import only_tailwind

individual_inputs = {
    "text": "text",
    "radioselect": "radio"
}

base_standalone = {
    "base": "base"
}

combined = {
    "base": "base",
    "text": "text",
    "radioselect": "radio"
}


def test_individual_input():
    container = CSSContainer(individual_inputs)
    assert container.text == "text"
    assert container.radioselect == "radio"
    assert container.checkbox == ""


def test_base_input():
    container = CSSContainer(base_standalone)
    for item in container.__dict__.values():
        assert item == "base"


def test_base_and_individual():
    container = CSSContainer(combined)
    assert "base" in container.text
    assert "text" in container.text
    assert "base" in container.radioselect
    assert "radio" in container.radioselect


def test_add_remove_extra_class():
    container = CSSContainer(base_standalone)
    container += individual_inputs
    assert "text" in container.text
    container -= individual_inputs
    assert "text" not in container.text


@only_tailwind
def test_form():
    form_helper = FormHelper()
    form_helper.css_container = CSSContainer(base_standalone)
    form_helper.layout = Layout(
        'first_name'
    )

    template = Template(
        """
        {% load crispy_forms_tags %}
        {% crispy form form_helper %}
        """
    )

    context = Context({"form": SampleForm(), "form_helper": form_helper})
    html = template.render(context)
    assert "base" in html
