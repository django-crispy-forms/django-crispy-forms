===================
django-crispy-forms
===================

The best way to have Django_ DRY forms. Build programmatic reusable layouts out of components, having full control of the rendered HTML without writing HTML in templates. All this without breaking the standard way of doing things in Django, so it plays nice with any other form application.

The application mainly provides:

* A filter named ``|crispy`` that will render elegant div based forms. Think of it as the built-in methods: ``as_table``, ``as_ul`` and ``as_p``. You cannot tune up the output, but it is easy to start using it. 
* A tag named ``{% crispy %}`` that will render a form based on your configuration and specific layout setup. This gives you amazing power without much hassle, helping you save tons of time.

By default all the templates were designed to work with `Uni-form`_, but you can create your own or use other bundles available, `see the docs`_ for more information.

.. _`see the docs`: http://django-crispy-forms.readthedocs.org/en/latest/index.html

Authors
=======

django-crispy-forms is the new django-uni-form. django-uni-form was an application created by `Daniel Greenfeld`_ that I leaded since version 0.8.0. The name change tries to better explain the purpose of the application, which changed in a significant way since its birth.

If you are upgrading from django-uni-form, we have `instructions`_ for helping you.

* Lead developer: `Miguel Araujo`_

.. _`Daniel Greenfeld`: https://github.com/pydanny
.. _`Miguel Araujo`: https://github.com/maraujop
.. _`instructions`: http://django-crispy-forms.readthedocs.org/en/latest/migration.html

Documentation
=============

For extensive documentation see the ``docs`` folder or `read it on readthedocs`_

.. _`read it on readthedocs`: http://django-crispy-forms.readthedocs.org/en/latest/index.html

Note
----

django-crispy-forms only supports Django 1.2 or higher and Python 2.5.4, Python 2.6.x and Python 2.7.x. If you need to support earlier versions of Django or Python you will need to use django-uni-form 0.7.0.

.. _`Uni-form`: http://sprawsm.com/uni-form
.. _Django: http://djangoproject.com
