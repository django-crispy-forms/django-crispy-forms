import os
import sys
import crispy_forms

from setuptools import setup, find_packages


if sys.argv[-1] == 'publish':
    if os.system("pip freeze | grep wheel"):
        print("wheel not installed.\nUse `pip install wheel`.\nExiting.")
        sys.exit()
    if os.system("pip freeze | grep twine"):
        print("twine not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (crispy_forms.__version__, crispy_forms.__version__))
    print("  git push --tags")
    sys.exit()

setup(
    name='django-crispy-forms',
    version=crispy_forms.__version__,
    description="Best way to have Django DRY forms",
    long_description=open('README.rst').read(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=['forms', 'django', 'crispy', 'DRY'],
    author='Miguel Araujo',
    author_email='miguel.araujo.perez@gmail.com',
    url='http://github.com/maraujop/django-crispy-forms',
    license='MIT',
    packages=find_packages(exclude=['docs']),
    include_package_data=True,
    zip_safe=False,
)
