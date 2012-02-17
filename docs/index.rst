.. django-crispy-forms documentation master file, created by
   sphinx-quickstart on Tue Nov  1 19:01:02 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Forms have never been this crispy
=================================

django-crispy-forms provides you with a ``|crispy`` filter and ``{% crispy %}`` tag that will let you control the rendering behavior of yours Django_ forms in a very elegant and DRY way. Have full control without writing custom form templates. All this without breaking the standard way of doing things in Django_, so it plays nice with any other form application.

User Guide
~~~~~~~~~~

Get the most out django-crispy-forms

.. toctree::
    :maxdepth: 2

    install
    migration
    filters
    tags

.. toctree::
    :maxdepth: 1

    customization
    faq
    contributors

* You can find a detailed history of the project in `Github's CHANGELOG`_

.. _`Github's CHANGELOG`: https://github.com/maraujop/django-crispy-forms/blob/dev/CHANGELOG.md

API documentation
~~~~~~~~~~~~~~~~~

If you are looking for information on a specific function, class or method, this part of the documentation is for you.

.. toctree::
    :maxdepth: 2
    
    api_helpers
    api_layout
    api_templatetags
   
Developer Guide
~~~~~~~~~~~~~~~

Think this is awesome and want to make it better? Read our contribution_ page, make it better, and we'll add you to the contributors_ list!

.. toctree::
    :maxdepth: 2

    contributing

.. _contribution: contributing.html
.. _contributors: contributors.html
.. _Django: http://djangoproject.com
