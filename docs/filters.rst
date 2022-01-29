crispy filter
=============

Crispy filter lets you render a form or formset using django-crispy-forms elegantly div based fields. Let's see a usage example::

    {% load crispy_forms_tags %}
    
    <form method="post" class="my-class">
        {{ my_formset|crispy }}
    </form>

1. Add ``{% load crispy_forms_tags %}`` to the template.
2. Append the ``|crispy`` filter to your form or formset context variable.
3. Refresh and enjoy!

Using {% crispy %} tag because it rocks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As handy as the `|crispy` filter is, think of it as the built-in methods: ``as_table``, ``as_ul`` and ``as_p``. You cannot tune up the output. The best way to make your forms crisp is using the :ref:`crispy tag forms`. It will change how you do forms in Django.

.. _`original implementation`: https://code.google.com/p/django-uni-form/source/browse/trunk/uni_form/templatetags/uni_form.py?spec=svn2&r=2
