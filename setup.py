from setuptools import setup, find_packages
 
version = '1.1.1'
 
setup(
    name='django-crispy-forms',
    version=version,
    description="Best way to have Django DRY forms",
    long_description=open('README.rst').read(),
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
    keywords=['forms', 'django', 'crispy', 'DRY'],
    author='Miguel Araujo',
    author_email='miguel.araujo.perez@gmail.com',
    url='http://github.com/maraujop/django-crispy-forms',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
