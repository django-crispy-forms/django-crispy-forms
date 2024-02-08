from crispy_forms.layout import Fieldset, Layout
from crispy_forms.utils import render_crispy_form

from .forms import SampleForm


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
