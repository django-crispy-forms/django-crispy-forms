# coding: utf-8
import pytest

from crispy_forms.layout import HTML, Div, Field, Fieldset, Layout, Submit

only_uni_form = pytest.mark.only('uni_form')
only_bootstrap = pytest.mark.only('bootstrap', 'bootstrap3', 'bootstrap4')
only_bootstrap3 = pytest.mark.only('bootstrap3')
only_bootstrap4 = pytest.mark.only('bootstrap4')


@pytest.fixture
def advanced_layout():
    return Layout(
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


@pytest.fixture(autouse=True, params=('uni_form', 'bootstrap', 'bootstrap3',
                                      'bootstrap4'))
def template_packs(request, settings):
    check_template_pack(request.node, request.param)
    settings.CRISPY_TEMPLATE_PACK = request.param


def check_template_pack(node, template_pack):
    mark = node.get_closest_marker('only')
    if mark:
        if template_pack not in mark.args:
            pytest.skip('Requires %s template pack' % ' or '.join(mark.args))
