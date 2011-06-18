====================
Absolute Basic Usage
====================

Using the as_uni_form filter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

At it's most basic level django-uni-form renders out the field elements of a form via the `as_uni_form` filter. The steps are simple:

1. Add ``{% load "uni_form_tags" %}`` to the template that calls your form.
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
    
.. note:: In the beginning, this was 100% of the `original implementation`_ of this project.

.. _`original implementation`: http://code.google.com/p/django-uni-form/source/browse/trunk/uni_form/templatetags/uni_form.py?spec=svn2&r=2

Using form helpers because they rock
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As handy as the `as_uni_form` filter is, the real advantage of this library are the :ref:`form helpers`. They will change how you do forms in Django.