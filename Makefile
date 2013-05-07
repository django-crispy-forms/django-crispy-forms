.PHONY: develop test

develop:
	pip install -q "file://`pwd`#egg=django-crispy-forms[tests]"
	pip install -q -e . --use-mirrors

test: develop
	cd crispy_forms/tests && python runtests.py