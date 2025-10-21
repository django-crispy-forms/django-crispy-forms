from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from crispy_forms.layout import HTML, Div, Field, Fieldset, Layout, Submit

if TYPE_CHECKING:
    from _pytest.fixtures import SubRequest
    from _pytest.python import Function
    from pytest_django.fixtures import SettingsWrapper


@pytest.fixture
def advanced_layout() -> Layout:
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


@pytest.fixture(autouse=True, params=(["bootstrap3"]))
def template_packs(request: SubRequest, settings: SettingsWrapper) -> None:
    check_template_pack(request.node, request.param)
    settings.CRISPY_TEMPLATE_PACK = request.param


def check_template_pack(node: Function, template_pack: str) -> None:
    mark = node.get_closest_marker("only")
    if mark:
        if template_pack not in mark.args:
            pytest.skip("Requires %s template pack" % " or ".join(mark.args))
