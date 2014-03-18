=====================================
How to create your own template packs
=====================================

First you will have to name your template pack, for this you can't use the name of one of the available template packs in crispy-forms, due to name collisions. For example, let's say in the company we work for, a designer has come up with a CSS bootstrap internally known as ``chocolat``. The company has a Django project that needs to start using ``chocolat``, therefore we need to create a folder named ``chocolat`` within our templates directory. Check your ``TEMPLATE_DIRS`` setting in Django and pick your preferred path.

Once we have that folder created, we will have to create a concrete directory hierarchy so that crispy-forms can pick it up. This is what bootstrap template pack (v2) looks like::

    .
    ├── accordion-group.html
    ├── accordion.html
    ├── betterform.html
    ├── display_form.html
    ├── errors.html
    ├── errors_formset.html
    ├── * field.html
    ├── layout
    │   ├── alert.html
    │   ├── * baseinput.html
    │   ├── button.html
    │   ├── checkboxselectmultiple.html
    │   ├── checkboxselectmultiple_inline.html
    │   ├── div.html
    │   ├── field_errors.html
    │   ├── field_errors_block.html
    │   ├── field_with_buttons.html
    │   ├── fieldset.html
    │   ├── formactions.html
    │   ├── help_text.html
    │   ├── help_text_and_errors.html
    │   ├── multifield.html
    │   ├── prepended_appended_text.html
    │   ├── radioselect.html
    │   ├── radioselect_inline.html
    │   ├── tab-link.html
    │   ├── tab.html
    │   └── uneditable_input.html
    ├── table_inline_formset.html
    ├── * uni_form.html
    ├── uni_formset.html
    ├── * whole_uni_form.html
    └── whole_uni_formset.html

Take it easy, don't panic, we won't need this many templates for our template pack. Templates are also quite simple to follow if you understand what problem crispy-forms solves. The bare minimum would be the templates marked with an asterisk.

Fundamentals
~~~~~~~~~~~~

First, since crispy-forms 1.5.0, template packs are self contained, you cannot reference a template from a different template pack.

crispy-forms has many features, but maybe you don't need your template pack to cover all of them. ``{% crispy %}`` templatetag renders forms using a global structure contained within ``whole_uni_form.html``. However, ``|crispy`` filter uses ``uni_form.html``. As you've probably guessed, the name of the templates comes from the old days of django-uni-form. Anyway, as an example, if we don't use ``|crispy`` filter, we don't really need to maintain a ``uni_form.html`` template within our template pack.

If we are planning on using formsets + ``{% crispy %}`` we will need a ``whole_uni_formset.html``, instead if we use formsets + ``|crispy`` we will need ``uni_formset.html``.

All of these templates use a tag named ``{% crispy_field %}`` that is loaded doing ``{% load crispy_forms_field %}``, that generates the html for ``<input>`` using ``field.html`` template, but previously doing Python preparation beforehand. In case you wonder the code for this tag lives in ``crispy_forms.templatetags.crispy_forms_field``, together with some other stuff.

So a template pack for a very basic example covering only forms and the usage of ``{% crispy %}`` tag, would need 2 templates: ``whole_uni_form.html``, ``field.html``. Well, that's not completely true, because every layout object has a template attached. So if we wanted to use ``Div``, we would need ``div.html``. Some are not that obvious, if you need ``Submit``, you will need ``baseinput.html``. Some layout objects, don't really have a template attached, like ``HTML``.

In the previous template tree, there are some templates that are there for DRY purposes, they are not really compulsory or part of a layout object, so don't worry too much.

Starting
~~~~~~~~

Now your best bet is probably start copying some or all of the templates under an existing crispy-forms template pack, such as ``bootstrap3``, then drop the ones you don't need. Next step is edit those templates, and adjust the HTML/CSS making it align with ``chocolat``, that sometimes means dropping/adding divs, classes and other stuff around. You can always create a form in your application, with a helper attached to that new template pack and start trying out your adaptation right away.

Currently, there is an existing template pack for crispy-forms that doesn't live in core, developed by David Thenon as an external pluggable application named `crispy-forms-foundation`_, it's also a good reference to check out.

Beware that crispy-forms evolves and adds new ``FormHelper.attributes``, if you want to use those in the future you will have to adapt your templates adding those variables and its handling.

.. _`crispy-forms-foundation`: https://github.com/sveetch/crispy-forms-foundation
