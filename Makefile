.PHONY: develop test

develop:
	python -m pip install -q -r requirements.txt
	python -m pip install -q -e .

test: develop
	DJANGO_SETTINGS_MODULE=crispy_forms.tests.test_settings py.test crispy_forms/tests --cov=crispy_forms