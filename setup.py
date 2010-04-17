from setuptools import setup, find_packages
 
version = '0.8.0'
 
LONG_DESCRIPTION = """
=====================================
django-uni-form (Django Uni-Form)
=====================================

Django (http://djangoproject.com ) forms are easily rendered as tables,
paragraphs, and unordered lists. However, elegantly rendered div based forms
is something you have to do by hand. The purpose of this application is to
provide a simple tag and/or filter that lets you quickly render forms in a div
format.

Uni-form (http://sprawsm.com/uni-form) has been selected as css/js library for
the design of the forms.
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
    url='http://github.com/pydanny/django-uni-form',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
