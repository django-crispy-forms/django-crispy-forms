============
Installation
============

Installing django-uni-form
~~~~~~~~~~~~~~~~~~~~~~~~~~

Install into your python path using pip or easy_install::

    pip install -U django-uni-form

Or if you are running earlier than Django_ 1.2 and/or Python 2.5::

    pip install django-uni-form==0.7.0
    
Add `uni_form` to your INSTALLED_APPS in settings.py::

    INSTALLED_APPS = (
        ...
        'uni_form',
    )
    
Dependencies
~~~~~~~~~~~~

Django-uni-form is a Django application that lets you build Django forms in a DRY programmatic way. By default the different components available, have been designed to be used in conjuction with `Uni-form`_, a CSS framework for form markup. You should understand that this has been done with the best intention. However, you are actually free to use default components as they are, without attaching `Uni-form`_ media files or you can customize templates from those components (ref).

If you want to use `Uni-form`_ with django-uni-form, depending on your setup, you may need to copy the static files to your local static folder::

    cp -r <location-of-django-uni-form>/uni_form/static/uni_form <directory-for-my-project's-static-files>

Displaying the static files
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you are using `Uni-form`_, it is recommended that you link a copy of jQuery, this will give some extra goodies. Preferably you should use a version hosted on Google's CDN servers since the user's browser might already have it cached.  (You can get the url for the latest version of jQuery at http://scriptsrc.net/.)  But there are some cases in which you'll want to host jQuery yourself, such as if you're doing development offline::

    <script src="{{ STATIC_URL }}js/jquery.js" type="text/javascript"></script>

Beyond jQuery, `Uni-form`_ requires three static files. You can see how we call them by looking in the `templates/uni_form/includes.html` file. You can call those files in several ways.

1. The best way is probably to copy this HTML into your templates. This allows you to make use of the CSS compressors that have been created by the Django community (http://www.djangopackages.com/grids/g/asset-managers/). Here's the HTML::

    <link rel="stylesheet" href="{{ STATIC_URL }}uni_form/uni-form.css" type="text/css" />
    <link rel="stylesheet" href="{{ STATIC_URL }}uni_form/default.uni-form.css" type="text/css" />
    <!-- note that there's also blue.uni-form.css and dark.uni-form.css available if you want to try changing defaults up -->
    <script src="{{ STATIC_URL }}uni_form/uni-form.jquery.js" type="text/javascript"></script>

2. Another way is to use Django's built-in **includes** template tag::

    {% include "uni_form/includes.html" %}
    
3. **ONLY FOR DJANGO 1.3 OR LATER** A third way is to use the django-uni-form **uni_form_setup** template tag.  Note that you'll need some additional setup for this::

    {% uni_form_setup %}

If you want to take advantage of the `{% uni_form_setup %}` tag, then you'll need to make sure `django.core.context_processors.request` is in the  TEMPLATE_CONTEXT_PROCESSORS tuple in your settings.py file::

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'django.core.context_processors.request',
    )


.. _Django: http://djangoproject.com
.. _`Uni-form`: http://sprawsm.com/uni-form
