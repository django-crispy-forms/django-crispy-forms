from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

from django.test.html import Element, parse_html

from crispy_forms.utils import render_crispy_form

if TYPE_CHECKING:
    from django.forms import BaseForm, BaseFormSet


TEST_DIR = os.path.dirname(os.path.abspath(__file__))


def parse_expected(expected_file: str) -> Element:
    test_file = Path(TEST_DIR) / "results" / expected_file
    with test_file.open() as f:
        return parse_html(f.read())


def parse_form(form: BaseForm | BaseFormSet[BaseForm]) -> Element:
    html = render_crispy_form(form)
    return parse_html(html)
