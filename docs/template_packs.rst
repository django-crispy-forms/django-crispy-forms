.. _template_packs:

=====================================
How to create your own template packs
=====================================

First you will have to name your template pack, for this you can't use the name of one of the available template packs in crispy-forms, due to name collisions. For example, let's say in the company we work for, a designer has come up with a CSS bootstrap internally known as ``chocolate``. The company has a Django project that needs to start using ``chocolate``, therefore we need to create a folder named ``chocolate`` within our templates directory. Check your ``TEMPLATE_DIRS`` setting in Django and pick your preferred path.

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

Now your best bet is probably start copying some or all of the templates under an existing crispy-forms template pack, such as ``bootstrap3``, then drop the ones you don't need. Next step is edit those templates, and adjust the HTML/CSS making it align with ``chocolate``, that sometimes means dropping/adding divs, classes and other stuff around. You can always create a form in your application, with a helper attached to that new template pack and start trying out your adaptation right away.

Currently, there is an existing template pack for crispy-forms that doesn't live in core, developed by David Thenon as an external pluggable application named `crispy-forms-foundation`_, it's also a good reference to check out.

Beware that crispy-forms evolves and adds new ``FormHelper.attributes``, if you want to use those in the future you will have to adapt your templates adding those variables and its handling.

.. _`crispy-forms-foundation`: https://github.com/sveetch/crispy-forms-foundation


*******************************
How to create your own template
*******************************

This 'how to' explains the steps required to create your own crispy-forms template for your own CSS framework. In this example we will build a template pack for `UIkit <https://getuikit.com/>`_.

Setup project and working environment
#####################################
To build our template pack we will copy an existing template pack and modify it to meet the requirements of the CSS framework. To test our template pack we will use   `crispy-test-project <https://github.com/django-crispy-forms/crispy-test-project>`_. This is a simple Django project which renders a number of forms and enables us to see the output of the template pack.

So let's begin by creating a new project.

1. Create a new project for our template pack

For our base template to develop from I am going to use the bootstrap 2 project. Let's clone it from GitHub. ::

``git clone https://github.com/django-crispy-forms/crispy-forms-bootstrap2``

We recommend that template packs are named using the convention 'crispy-forms-"template pack name". In this case we will call it `crispy-forms-uikit`.

Next step is to make the change to rename the project. Files where changes are required are:

- Folder names
- setup.py
- README.md
- MANIFEST.IN
- Makefile
- layout.py (TEMPLATE_PACK)
- test files
- template files (e.g. ``whole_uni_form.html``)


In addition a few of the test files will need changes:

- Add your template pack as an allowed template pack in the test_setting.py file e.g.CRISPY_ALLOWED_TEMPLATE_PACKS = 'uikit'
- In `test_utils.py` change line 51 to use your new template pack
- In `test_form_helper` remove the two template_pack_override tests as we only have one template

To test this works now run ``make test`` and confirm the test suite passes.

2. Setup crispy-test-project

Now lets setup crispy-test-project

Create a separate folder for crispy-test-project and clone the repo. ::

``git clone https://github.com/django-crispy-forms/crispy-test-project``

Navigate into the folder and install the package::

``cd crispy-test-project``
``pipenv install``

This will create a virtual environment and install all of the dependencies

Finally install the development version of your template package (to the directory of your setup.py file)::

``pip install -e /path/to/package``

Our development environment is now all setup up so we can move onto making the changes for our own CSS template pack.

The test project comes with a number of pages to demonstrate the capability for a number of template packs. You can either new page to develop your template pack or modify one of the existing pages. I will be manipulating the standard 'Django Rendering' page to meet the requirements of my template pack.

To setup a template page we need to:

- Add the CSS & JS links for your template pack to the base.html file
- In settings.py:
    - Add your template pack to ``INSTALLED_APPS``
    - Enable your template pack by setting ``CRISPY_TEMPLATE_PACK``
    - Include your template pack in ``CRISPY_ALLOWED_TEMPLATE_PACKS``

Customise template pack
#######################

The boostrap template pack we copied is mature and has a number of templates for many different features of boostrap. In additon Crispy forms has many features which require different templates. To start with we will be building capability for crispy forms to use {% crispy %} templatetags and no form sets. To do this the minimum files we require to update are ``whole_uni_form.html``, ``field.html`` and ``baseinput.html``.

Note:
Most of our inputs will probably be rendered by passing css classes to ``Django`` and using their templates. ``baseinput.html`` is ONLY for buttons (e.g. submit).

Finally, we get to the development of our new template pack. The techniques required will vary from template pack to template pack. The below therefore explains the techniques I used to create a template pack. This will provide the tools to use in building a template pack for your own CSS framework.

1. Input classes.

The first change I'm going to make is to add a css class to all of the ``<input>`` elements. As mentioned before crispy-forms passes some of the html generation to Django and this is one of those cases. This customisation is enabled through a setting in the settings.py file rather than a change to the template pack.

For this you need to use a settings variable called ``CRISPY_CLASS_CONVERTERS``, expected to be a Python dictionary::

        CRISPY_CLASS_CONVERTERS = {
            'textinput': 'uk-input',
            'textarea': 'uk-textarea',
            'select': 'uk-select',
            'checkboxinput': 'uk-checkbox',
        }

For example this setting would generate ``<input type="text" class="uk-input"``. The key of the dictionary ``textinput`` is the Django's default class, the value is what you want it to be substituted with, in this case we are using ``uk-input``.

2. field.html

This file contains the logic on how to render the standard field types. (i.e. input, checkbox, radio). As bootstrap is complex you may be able to simplify this file if the css for your template pack is less complex. e.g. for boostrap there are special layout files to generate the html required for the various options on checkbox and radios.

3. Labels

CSS for the labels is most likely to be in the ``field.html`` file, or if you need a more complex html layout in the appropriate layout file.

For UIkit I simply changed the CSS code for labels in the field.html file.

4. Help text

Bootstrap is complex and has different layout files for help and error messages. I could choose to simplify the number of layout files by re-writeing ``field.html`` file to build in the layout for help and error messages or I could retrain the existing logic. For simplicity I will change the CSS style in the appropriate layout files (e.g. help_text.html, and field_errors.html).

The help text is also a good example of where you can become opinionated and use the power of crispy-forms to develop your forms in a DRY way. You can become opinionated about the layout of help messages and only have to code this once.

5. Radios and checkbox

The bootstrap pack provides layout files for checkbox and radio. For your CSS pack you may be able to not use these and just default django styles but most likely you will need some extra HTML layout and CSS classes for these elements.

For UIkit I used the existing template packs and added the required CSS to the div, label and input tags. Some CSS tags may be dependant upon the layout required, you can add logic into your templates using {% %} tags. In the case for UIKit I needed to add ``uk-form-stacked`` to stacked forms but not for inline. I therefore added the following to the appropriate div::

      {% if not inline_class %} uk-form-stacked {% endif %}


