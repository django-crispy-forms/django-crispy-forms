============
Installation
============

.. _`install`:

Installing django-crispy-forms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install latest stable version into your python environment using pip::

    pip install django-crispy-forms

If you want to install development version (unstable), you can do so doing::

    pip install git+git://github.com/django-crispy-forms/django-crispy-forms.git@main#egg=django-crispy-forms

Or, if you'd like to install the development version as a git repository (so
you can ``git pull`` updates), use the ``-e`` flag with ``pip install``, like
so:: 

    pip install -e git+git://github.com/django-crispy-forms/django-crispy-forms.git@main#egg=django-crispy-forms

Once installed add ``crispy_forms`` to your ``INSTALLED_APPS`` in settings.py::

    INSTALLED_APPS = (
        ...
        'crispy_forms',
    )

In production environments, always activate Django template cache loader. This is available since Django 1.2 and what it does is basically load templates once, then cache the result for every subsequent render. This leads to a significant performance improvement. To see how to set it up refer to the fabulous `Django docs page`_.

.. _`Django docs page`: https://docs.djangoproject.com/en/2.2/ref/templates/api/#django.template.loaders.cached.Loader

Template packs
~~~~~~~~~~~~~~
Since version 2.0, django-crispy-forms template packs are now in separate packages.

You will need to install the appropriate template pack for your CSS framework and add it to your list of ``INSTALLED_APPS``. The the following template packs have been extracted from crispy-forms core are now available on PyPI.

* ``Bootstrap2`` `crispy-forms-bootstrap2`_.
* ``Bootstrap3`` `crispy-bootstrap3`_.
* ``Bootstrap4`` `crispy-bootstrap4`_.

Version v1.x also provided template packs for:

* ``uni-form`` `Uni-form`_ is a nice looking, well structured, highly customizable, accessible and usable forms.

In addition the following template packs are available through separately maintained projects.

* ``foundation`` `Foundation`_ In the creator's words, "The most advanced responsive front-end framework in the world." This template pack is available through `crispy-forms-foundation`_
* ``tailwind`` `Tailwind`_ A utility first framework. This template pack is available through `crispy-tailwind`_
* ``Bootstrap 5`` Support for newer versions of Bootstrap will be in separate template packs. This starts with version 5 and is available through `crispy-bootstrap5`_
* ``Bulma`` `Bulma`_: the modern CSS framework that just works. This template pack is available through `crispy-bulma`_

If your form CSS framework is not supported and it's open source, you can create a ``crispy-forms-templatePackName`` project. Please let me know, so I can link to it. Documentation on :ref:`template_packs` is provided.

You can set your default template pack for your project using the ``CRISPY_TEMPLATE_PACK`` Django settings variable::

    CRISPY_TEMPLATE_PACK = 'uni_form'

Please check the documentation of your template pack package for the correct value of the ``CRISPY_TEMPLATE_PACK`` setting (there are packages which provide more than one template pack).

.. _`Bootstrap`: https://getbootstrap.com
.. _`Bulma`: https://bulma.io
.. _`Foundation`: https://get.foundation
.. _`crispy-forms-foundation`: https://github.com/sveetch/crispy-forms-foundation
.. _`Tailwind`: https://tailwindcss.com
.. _`crispy-tailwind`: https://github.com/django-crispy-forms/crispy-tailwind
.. _`crispy-forms-bootstrap2`: https://pypi.org/project/crispy-forms-bootstrap2/
.. _`crispy-bootstrap3`: https://pypi.org/project/crispy-bootstrap3/
.. _`crispy-bootstrap4`: https://pypi.org/project/crispy-bootstrap4/
.. _`crispy-bootstrap5`: https://github.com/django-crispy-forms/crispy-bootstrap5
.. _`crispy-bulma`: https://github.com/ckrybus/crispy-bulma

Setting static files
~~~~~~~~~~~~~~~~~~~~

crispy-forms does not include static files. You will need to include the proper corresponding static files yourself depending on what CSS framework (Template pack) you are using. This might involve one or more CSS and JS files. Read CSS framework's docs for help on how to set it up.
 

.. _Django: https://djangoproject.com
.. _`Uni-form`: https://github.com/draganbabic/uni-form/tree/uni-form-v-1-5
