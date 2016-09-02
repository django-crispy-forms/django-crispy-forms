============
Installation
============

.. _`install`:

Installing django-crispy-forms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install latest stable version into your python path using pip or easy_install::

    pip install --upgrade django-crispy-forms

If you want to install development version (unstable), you can do so doing::

    pip install git+git://github.com/maraujop/django-crispy-forms.git@dev#egg=django-crispy-forms

Or, if you'd like to install the development version as a git repository (so
you can ``git pull`` updates, use the ``-e`` flag with ``pip install``, like
so:: 

    pip install -e git+git://github.com/maraujop/django-crispy-forms.git@dev#egg=django-crispy-forms

Add ``crispy_forms`` to your ``INSTALLED_APPS`` in settings.py::

    INSTALLED_APPS = (
        ...
        'crispy_forms',
    )

In production environments, always activate Django template cache loader. This is available since Django 1.2 and what it does is basically load templates once, then cache the result for every subsequent render. This leads to a significant performance improvement. See how to set it up using fabulous `Django docs page`_.

.. _`Django docs page`: https://docs.djangoproject.com/en/1.5/ref/templates/api/#django.template.loaders.cached.Loader

Template packs
~~~~~~~~~~~~~~

Since version 1.1.0, django-crispy-forms has built-in support for different CSS frameworks, known as template packs within django-crispy-forms:

* ``bootstrap`` `Bootstrap`_ is crispy-forms's default template pack, version 2 of the popular simple and flexible HTML, CSS, and Javascript for user interfaces from Twitter.
* ``bootstrap3`` Twitter Bootstrap version 3.
* ``uni-form`` `Uni-form`_ is a nice looking, well structured, highly customizable, accessible and usable forms.
* ``foundation`` `Foundation`_ In the creator's words, "The most advanced responsive front-end framework in the world." This template pack is externally available through `crispy-forms-foundation`_

If your form CSS framework is not supported and it's open source, you can create a template pack for it and submit a pull request in Github or create a ``crispy-forms-templatePackName`` project and let me know, so I can link it.

You can set your default template pack for your project using the ``CRISPY_TEMPLATE_PACK`` Django settings variable::

    CRISPY_TEMPLATE_PACK = 'uni_form'

Please check the documentation of your template pack package for the correct value of the ``CRISPY_TEMPLATE_PACK`` setting (there are packages which provide more than one template pack).

.. _`Bootstrap`: http://twitter.github.com/bootstrap/index.html
.. _`Foundation`: http://foundation.zurb.com/
.. _`crispy-forms-foundation`: https://github.com/sveetch/crispy-forms-foundation

Setting media files
~~~~~~~~~~~~~~~~~~~

crispy-forms no longer includes static files. You will need to include the proper corresponding media files yourself depending on what CSS framework (Template pack) you are using. This might involve one or more CSS and JS files. Read CSS framework's docs for help on how to set it up.

Moving from django-uni-form to django-crispy-forms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

django-crispy-forms was started as a friendly fork of django-uni-form. We are aware that a name change implies some hassle updating imports and templates, here is some help mitigating it. This is what you should replace when upgrading:

1. Your ``INSTALLED_APPS`` should point to ``crispy_forms`` instead of ``uni_form``

2. All imports have to be done from crispy forms::

    from uni_form.helper import FormHelper
    from crispy_forms.helper import FormHelper

In Linux You can use `rpl`_ to easily find and update the proper lines. In the root of your project run the following command. It is strongly recommended that you have your project in a VCS or a backup, so you can rollback if something goes wrong::

    rpl -R uni_form. crispy_forms. .

.. _`rpl`: http://www.laffeycomputer.com/rpl.html

3. All tags loading needs to be updated::

    {% load uni_form_tags %}
    {% load crispy_forms_tags %}

Using rpl::

    rpl -R "{% load uni_form_tags %}" "{% load crispy_forms_tags %}" .

4. Until version 1.2.0 former tags and filters names worked without changing them, current versions will force updating your filters and tags::

    |as_uni_form -----> |crispy
    {% uni_form %} ---> {% crispy %}
    |as_uni_errors ---> |as_crispy_errors
    |as_uni_field ----> |as_crispy_field

Using rpl::

    rpl -R "|as_uni_form" "|crispy" .
    rpl -R "{% uni_form" "{% crispy" .
    rpl -R "|as_uni_errors" "|as_crispy_errors" .
    rpl -R "|as_uni_field" "|as_crispy_field" .

There is one filter that has been turned into a tag for extra layout power, so the former filter name will not work. You will only need to update this if you have custom or overridden templates in your project::

    field|with_class ------> {% crispy_field field %}

5. If you have ``UNIFORM_FAIL_SILENTLY`` setting variable defined, you have to rename it to ``CRISPY_FAIL_SILENTLY``.

6. crispy-forms renders your layouts strictly, exactly the fields mentioned, if you want crispy-forms to work the same way as django-uni-form you can set new ``FormHelper`` attribute ``render_unmentioned_fields`` to ``True``.


Uni-form static files
~~~~~~~~~~~~~~~~~~~~~

`Uni-form`_ files are composed of two CSS files and one JS library based on jQuery. Uni-form's JS library provides some nice interactions, but you will need to link a copy of jQuery. Preferably you should use a `version hosted`_ on Google's CDN servers since the user's browser might already have it cached.

.. _`version hosted`: http://scriptsrc.net/.

For linking `Uni-form`_ static files add the proper lines to your HTML head. This is an example on how to do it if you are using ``STATIC_URL``::

    <!-- note that there's also blue.uni-form.css and dark.uni-form.css available if you want to try changing defaults up -->
    <link rel="stylesheet" href="{{ STATIC_URL }}uni_form/uni-form.css" type="text/css" />
    <link rel="stylesheet" href="{{ STATIC_URL }}uni_form/default.uni-form.css" type="text/css" />
    <!-- uni-form JS library, optional -->
    <script src="{{ STATIC_URL }}uni_form/uni-form.jquery.js" type="text/javascript"></script>

Activate uni-form.jquery
~~~~~~~~~~~~~~~~~~~~~~~~

If you link `Uni-form`_ JS library do not forget to activate given forms::

    <script>
      $(function(){
        $('form.uniForm').uniform();
      });
    </script>


.. _Django: http://djangoproject.com
.. _`Uni-form`: http://sprawsm.com/uni-form
