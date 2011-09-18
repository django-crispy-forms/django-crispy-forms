===============
django-uni-form
===============

The best way to have Django_ DRY forms. Build programmatic reusable layouts out of components, having full control of the rendered HTML. All this without breaking the standard way of doing things in Django, so it plays nice with any other form application.

The application mainly provides:

* A filter named ``|as_uni_form`` that will render elegant div based forms. Think of it as the built-in methods: ``as_table``, ``as_ul`` and ``as_p``. You cannot tune up the output, but it is easy to start using. 
* A tag named ``{% uni_form %}`` that will render a form based on your configuration and specific layout setup. This gives you amazing power without much hassle, helping you save tons of time. 

By default all the templates were designed to work with `Uni-form`_, but you can create your own or use other bundles available, `see the docs`_ for more information.

.. _`see the docs`: http://readthedocs.org/docs/django-uni-form/en/latest/

Authors
=======

* Author: `Daniel Greenfeld`_
* Lead developer: `Miguel Araujo`_

.. _`Daniel Greenfeld`: https://github.com/pydanny
.. _`Miguel Araujo`: https://github.com/maraujop

Documentation
=============

For extensive documentation see the ``docs`` folder or `read it on readthedocs`_

.. _`read it on readthedocs`: http://readthedocs.org/docs/django-uni-form/en/latest/

Note
----

django-uni-form only supports Django 1.2 or higher and Python 2.5.4, Python 2.6.x and Python 2.7.x. If you need to support earlier versions of Django or Python you will need to use django-uni-form 0.7.0.

.. _`Uni-form`: http://sprawsm.com/uni-form
.. _Django: http://djangoproject.com
