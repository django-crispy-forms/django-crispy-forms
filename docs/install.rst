============
Installation
============

Installing django-crispy-forms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install latest stable version into your python path using pip or easy_install::

    pip install --upgrade django-crispy-forms

If you want to install development version (unstable), you can do so doing::

    pip install django-crispy-forms==dev

Add ``crispy_forms`` to your ``INSTALLED_APPS`` in settings.py::

    INSTALLED_APPS = (
        ...
        'crispy_forms',
    )
    
Template packs
~~~~~~~~~~~~~~

Since version 1.1.0 of django-crispy-forms has built-in support for two different CSS frameworks, known as template packs within django-crispy-forms:

* `Bootstrap`_ The default template pack. The popular simple and flexible HTML, CSS, and Javascript for user interfaces from Twitter.
* `Uni-form`_ Nice looking, well structured, highly customizable, accessible and usable forms.

If your form CSS framework is not supported, you can create a template pack for it and submit a pull request in github. You can easily switch between both using ``CRISPY_TEMPLATE_PACK`` setting variable, setting it to ``bootstrap`` or ``uni_form``.

.. _`Uni-form`: http://sprawsm.com/uni-form
.. _`Bootstrap`: http://twitter.github.com/bootstrap/index.html

Setting media files 
~~~~~~~~~~~~~~~~~~~

You will need to include the proper media files, depending on what CSS framework you are using. This might involve one or more CSS and JS files. Read CSS framework's docs for help on how to set it up.

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
