.PHONY: develop test

develop:
	pip install -q -r requirements.txt
	pip install -q -e .

test: develop
	DJANGO_SETTINGS_MODULE=tests.test_settings py.test tests --cov=crispy_forms