from setuptools import setup, find_packages
 
version = '0.9.0'
 
LONG_DESCRIPTION = """
=====================================
django-uni-form (django-uni-form)
=====================================

Django_ forms are easily rendered as tables,
paragraphs, and unordered lists. However, elegantly rendered div based forms
is something you have to do by hand. The purpose of this application is to
provide a simple tag and/or filter that lets you quickly render forms in a div
format.

`Uni-form`_ has been selected as the base model for the design of the forms.

Documentation
=============

http://readthedocs.org/docs/django-uni-form/en/latest/

.. note:: django-uni-form only supports Django 1.2 or higher and Python
2.5.4, Python 2.6.x and Python 2.7.x. If you need to support earlier versions
of Django or Python you will need to use django-uni-form 0.7.0.


.. _`Uni-form`: http://sprawsm.com/uni-form
.. _Django: http://djangoproject.com
"""
 
setup(
    name='django-uni-form',
    version=version,
    description="django-uni-form",
    long_description=LONG_DESCRIPTION,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
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
