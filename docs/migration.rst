Moving from django-uni-form to django-crispy-forms
==================================================

We are aware that a name change implies some hassle updating imports and templates. This is what you should replace when upgrading:

1. Your ``ÌNSTALLED_APPS`` should point to ``crispy_forms`` instead of ``uni_form``

2. All imports have to be done from crispy forms::

    from uni_form.helper import FormHelper 
    from crispy_forms.helper import FormHelper

In Linux You can use `rpl`_ to easily find and update the proper lines. Run in the root of your project the following command. It is strongly recommended that you have your project in a VCS or a backup, so you can rollback if something goes wrong::

    rpl -R uni_form. crispy_forms. .

.. _`rpl`: http://www.laffeycomputer.com/rpl.html

3. All tags loading needs to be updated::

    {% load uni_form_tags %}
    {% load crispy_forms_tags %}

Using rpl::
    
    rpl -R "{% load uni_form_tags %}" "{% load crispy_forms_tags %}" .

4. Until version 1.2.0 former tags and filters names will work. However you should also think of updating your filters and tags::

    |as_uni_form -----> |crispy
    {% uni_form %} ---> {% crispy %}
    |as_uni_errors ---> |as_crispy_errors
    |as_uni_field ----> |as_crispy_field

Using rpl::

    rpl -R "|as_uni_form" "|crispy" .
    rpl -R "{% uni_form" "{% crispy" .
    rpl -R "|as_uni_errors" "|as_crispy_errors" .
    rpl -R "|as_uni_field" "|as_crispy_field" .

There is one filter that has been turned into a tag for extra layout power, so former filter name will not work. You will only need to update this if you have custom or overriden templates in your project::

    field|with_class ------> {% crispy_field field %}

5. If you have ``UNIFORM_FAIL_SILENTLY`` setting variable defined, you have to rename it to ``CRISPY_FAIL_SILENTLY``.
