from setuptools import setup, find_packages
 
version = '0.7.0'
 
LONG_DESCRIPTION = """
=====================================
django-uni-form (Django Uni-Form)
=====================================

Django (http://djangoproject.com ) forms are easily rendered as tables,
paragraphs, and unordered lists. However, elegantly rendered div based forms
is something you have to do by hand. The purpose of this application is to
provide a simple tag and/or filter that lets you quickly render forms in a div
format.

Uni-form (http://sprawsm.com/uni-form) has been selected as the base model for
the design of the forms.

This release includes:

 * Removed a <hr /> from the layout module.
 * Changed templatetags/uni_form.py to templatetags/uni_form_tags.py. Yes, this breaks backwards compatibility but fixes a namespace problems in Django with naming a templatetag library after the parent application.
 * Changed form_action attribute to accept not just named URLs but also any old URL.
 * Added in uni_form_setup tag.
 * Added tests
 * Added several new contributors including Dragan Babic
 * Added Danish language translation
"""
 
setup(
    name='django-uni-form',
    version=version,
    description="django-uni-form",
    long_description=LONG_DESCRIPTION,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
    keywords='forms,django',
    author='Daniel Greenfeld',
    author_email='pydanny@gmail.com',
    url='http://github.com/pydanny/django-uni-form/tree/master',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    setup_requires=['setuptools_git'],
)
