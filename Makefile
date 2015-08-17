.PHONY: develop test

develop:
	pip install -q -r requirements.txt
	pip install -q -e .

test: develop
	pip install pytest pytest-django
	cd crispy_forms/tests && python runtests.py