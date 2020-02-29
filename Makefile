.PHONY: develop test

develop:
	pip3 install -q -r requirements.txt
	pip3 install -q -e .

test: develop
	coverage run -m pytest --ds=crispy_forms.tests.test_settings
