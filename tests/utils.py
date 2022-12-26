import os
from pathlib import Path

from django.test.html import parse_html

from crispy_forms.utils import render_crispy_form

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


def parse_expected(expected_file):
    test_file = Path(TEST_DIR) / "results" / expected_file
    with test_file.open() as f:
        return parse_html(f.read())


def parse_form(form):
    html = render_crispy_form(form)
    return parse_html(html)
