===============
Usage: Filters
===============

Still quite useful, this is a improved and evolved version of the `original implementation`_ of the django-uni-form project.

Using the filter (Easy and fun!)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Add ``{% load uni_form_filters %}`` to the template that calls your form.
2. Append your form call with the as_uni_form filter::

    {{ my_form|as_uni_form }}

3. Add the class of 'uniForm' to your form. Example::

    <form action="" method="post" class="uniForm">

4. Refresh and enjoy!

To see this more clearly::

    {% extends "uni_form" %}
    
    <form method="post" class="uniForm">

        {{ my_form|as_uni_form }}

    </form>

.. _`original implementation`: http://code.google.com/p/django-uni-form/source/browse/trunk/uni_form/templatetags/uni_form.py?spec=svn2&r=2