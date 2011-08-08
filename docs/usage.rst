====================
|as_uni_form filter
====================

Usage
~~~~~

Django-uni-form provides a filter called `as_uni_form`, that lets you render a form or formset using django-uni-form elegantly div based fields. The steps are simple:

1. Add ``{% load uni_form_tags %}`` to the template.
2. Append the as_uni_form filter to your form::

    {{ my_form|as_uni_form }}

3. Add the class of 'uniForm' to your form. Example::

    <form action="" method="post" class="uniForm">

4. Refresh and enjoy!

To see this more clearly, let's see a formset example all together::

    {% load uni_form_tags %}
    
    <form method="post" class="uniForm">
        {{ my_formset|as_uni_form }}
    </form>
    
.. note:: In the beginning, this was 100% of the `original implementation`_ of this project.


Using {% uni_form %} tag because it rocks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As handy as the `as_uni_form` filter is, the real advantage of this library are the :ref:`form helpers`. They will change how you do forms in Django.


.. _`original implementation`: http://code.google.com/p/django-uni-form/source/browse/trunk/uni_form/templatetags/uni_form.py?spec=svn2&r=2