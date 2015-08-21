# coding: utf-8
import pytest

from crispy_forms.layout import Layout, Div, Field, Submit, Fieldset, HTML


only_uni_form = pytest.mark.only('uni_form')
only_bootstrap = pytest.mark.only('bootstrap', 'bootstrap3')
only_bootstrap3 = pytest.mark.only('bootstrap3')


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


@pytest.fixture(autouse=True, params=('uni_form', 'bootstrap', 'bootstrap3'))
def template_packs(request, settings):
    check_template_pack(request._pyfuncitem._obj, request.param)
    settings.CRISPY_TEMPLATE_PACK = request.param


def check_template_pack(function, template_pack):
    if hasattr(function, 'only'):
        mark = function.only
        if template_pack not in mark.args:
            pytest.skip('Requires %s template pack' % ' or '.join(mark.args))
