============
Installation
============

Installing django-crispy-forms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install into your python path using pip or easy_install::

    pip install --upgrade django-crispy-forms

Add `crispy_forms` to your INSTALLED_APPS in settings.py::

    INSTALLED_APPS = (
        ...
        'crispy_forms',
    )
    
Dependencies
~~~~~~~~~~~~

Django-crispy-forms uses by default `Uni-form`_ (a CSS framework for form markup) templates. However, you are actually free to use any other CSS form framework. 

Setting uni-form templates 
~~~~~~~~~~~~~~~~~~~~~~~~~~

For using default `Uni-form`_ templates, you will need to include the proper media files. django-crispy-forms comes with the necessary files in a directory named static. Depending on your setup, you may need to copy those files to your local static folder::

    cp -r <location-of-django-crispy-forms>/crispy_forms/static/uni_form <directory-for-my-project's-static-files>

Displaying uni-form static files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Uni-form`_ files are composed of two CSS files and one JS library based on jQuery. Uni-form's JS library provides some nice interactions, but you will need to link a copy of jQuery. Preferably you should use a `version hosted`_ on Google's CDN servers since the user's browser might already have it cached.

.. _`version hosted`: http://scriptsrc.net/.

For linking `Uni-form`_ static files add the proper lines to your HTML head. This is an example on how to do it if you are using `STATIC_URL`::

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
