crispy filter
=============

Crispy filter lets you render a form or formset using django-crispy-forms elegantly div based fields. Let's see a usage example::

    {% load uni_form_tags %}
    
    <form method="post" class="uniForm">
        {{ my_formset|crispy }}
    </form>

1. Add `{% load uni_form_tags %}` to the template.
2. Append the `|crispy` filter to your form or formset context variable.
3. Add the class of 'uniForm' to your form.
4. Refresh and enjoy!

Using {% crispy %} tag because it rocks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As handy as the `|crispy` filter is, the best way to make your forms crisp is using the :ref:`form helpers`. It will change how you do forms in Django.

.. _`original implementation`: http://code.google.com/p/django-uni-form/source/browse/trunk/uni_form/templatetags/uni_form.py?spec=svn2&r=2
