.PHONY: develop test

develop:
	pip install -q -r requirements.txt
	pip install -q -e .

test: develop
	cd crispy_forms/tests && python runtests.py