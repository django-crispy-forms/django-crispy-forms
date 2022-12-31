import pytest

from crispy_forms.layout import HTML, Div, Field, Fieldset, Layout, Submit


@pytest.fixture
def advanced_layout():
    return Layout(
        Div(
            Div(Div("email")),
            Div(Field("password1")),
            Submit("save", "save"),
            Fieldset(
                "legend",
                "first_name",
                HTML("extra text"),
            ),
            Layout("password2"),
        ),
        "last_name",
    )
