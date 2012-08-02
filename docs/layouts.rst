=======
Layouts
=======

Fundamentals
~~~~~~~~~~~~

Django-crispy-forms defines another powerful class called ``Layout``, which allows you to change the way the form fields are rendered. This allows you to set the order of the fields, wrap them in divs or other structures, add html, set ids, classes or attributes to whatever you want, etc. And all that without writing a custom form template, using programmatic layouts. Just attach the layout to a helper, layouts are optional, but probably the most powerful thing django-crispy-forms has to offer.

A ``Layout`` is constructed by layout objects, which can be thought of as form components. You assemble your layout using those. For the time being, your choices are: ``ButtonHolder``, ``Button``, ``Div``, ``Row``, ``Column``, ``Fieldset``, ``MultiField``, ``HTML``, ``TemplateInclude``, ``Hidden``, ``Reset``, ``Submit``, ``Field``, ``AppendedText``, ``PrependedText``, ``FormActions``.

All these components are explained later in :ref:`layout objects`. What you need to know now about them is that every component renders a different template and has a different purpose. Let’s write a couple of different layouts for our form, continuing with our form class example (note that the full form is not shown again).

Some layout objects are specific to a template pack. For example ``ButtonHolder`` is for ``uni_form`` template_pack, while ``FormActions`` is for ``bootstrap`` template pack.

Let's add a layout to our helper::

    from crispy_forms.helper import FormHelper
    from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

    class ExampleForm(forms.Form):
        [...]
        def __init__(self, *args, **kwargs):
            self.helper = FormHelper()
            self.helper.layout = Layout(
                Fieldset(
                    'first arg is the legend of the fieldset',
                    'like_website',
                    'favorite_number',
                    'favorite_color',
                    'favorite_food',
                    'notes'
                ),
                ButtonHolder(
                    Submit('submit', 'Submit', css_class='button white')
                )
            )
            super(ExampleForm, self).__init__(*args, **kwargs)

When we render the form now using::

    {% load crispy_forms_tags %}
    {% crispy example_form %}

We will get the fields wrapped in a fieldset, whose legend will be set to 'first arg is the legend of the fieldset'. The fields' order will be: ``like_website``, ``favorite_number``, ``favorite_color``, ``favorite_food`` and ``notes``. We also get a submit button wrapped in a ``<div class="buttonHolder">`` which uni-form CSS positions in a nice way. That button has its CSS class set to ``button white``.

This is just the tip of the iceberg: now imagine you want to add an explanation for what notes are, you can use ``HTML`` layout object::

    Layout(
        Fieldset(
            'Tell us your favorite stuff {{ username }}',
            'like_website',
            'favorite_number',
            'favorite_color',
            'favorite_food',
            HTML("""
                <p>We use notes to get better, <strong>please help us {{ username }}</strong></p>
            """),
            'notes'
        )
    )

As you'll notice the fieldset legend is context aware and you can write it as if it were a chunk of a template where the form will be rendered. The ``HTML`` object will add a message before the notes input and it's also context aware. Note how you can wrap layout objects into other layout objects. Layout objects ``Fieldset``, ``Div``, ``MultiField`` and ``ButtonHolder`` can hold other Layout objects within. Let's do an alternative layout for the same form::

    Layout(
        MultiField(
            'Tell us your favorite stuff {{ username }}',
            Div(
                'like_website',
                'favorite_number',
                css_id = 'special-fields'
            ),
            'favorite_color',
            'favorite_food',
            'notes'
        )
    )

This time we are using a ``MultiField``, which is a layout object that as a general rule can be used in the same places as ``Fieldset``. The main difference is that this renders all the fields wrapped in a div and when there are errors in the form submission, they are shown in a list instead of each one surrounding the field. Sometimes the best way to see what layout objects do, is just try them and play with them a little bit.


.. _`layout objects`:

Universal layout objects
~~~~~~~~~~~~~~~~~~~~~~~~

These ones live in module ``crispy_forms.layout``. These are layout objects that are not specific to a template pack. We'll go one by one, showing usage examples:

- **Div**: It wraps fields in a ``<div>``::

    Div('form_field_1', 'form_field_2', 'form_field_3', ...)

**NOTE** Mainly in all layout objects you can set kwargs that will be used as HTML attributes. As ``class`` is a reserved keyword in Python, for it you will have to use ``css_class``. For example::

    Div('form_field_1', style="background: white;", title="Explication title", css_class="bigdivs")

- **HTML**: A very powerful layout object. Use it to render pure html code. In fact it behaves as a Django template and it has access to the whole context of the page where the form is being rendered. This layout object doesn't accept any extra parameters than the html to render, you cannot set html attributes like in ``Div``::

    HTML("{% if success %} <p>Operation was successful</p> {% endif %}")

- **Field**: Extremely useful layout object. You can use it to set attributes in a field or render a specific field with a custom template. This way you avoid having to explicitly override the field's widget and pass an ugly ``attrs`` dictionary::

    Field('password', id="password-field", css_class="passwordfields", title="Explanation")
    Field('slider', template="custom-slider.html")

This layout object can be used to easily extend Django's widgets.

- **Submit**: Used to create a submit button. First parameter is the ``name`` attribute of the button, second parameter is the ``value`` attribute::

    Submit('search', 'SEARCH')
    Submit('search', 'SEARCH')

Renders to::

    <input type="submit" name="search" value="SEARCH" class="submit submitButton" id="submit-id-search" />

- **Hidden**: Used to create a hidden input::

    Hidden('name', 'value')

- **Button**: Creates a button::

    Button('name', 'value')

- **Reset**: Used to create a reset input::

    reset = Reset('name', 'value')

- **Fieldset**: It wraps fields in a ``<fieldset>``. The first parameter is the text for the fieldset legend, as we've said it behaves like a Django template::

    Fieldset("Text for the legend {{ username }}",
        'form_field_1',
        'form_field_2'
    )

Uni-form layout objects
~~~~~~~~~~~~~~~~~~~~~~~

These ones live in module ``crispy_forms.layout``. Probably in the future they will be moved out to a ``uni_form`` module:

- **ButtonHolder**: It wraps fields in a ``<div class=”buttonHolder”>``, which uni-form positions in a nice way. This is where form's submit buttons go in uni-form::

    ButtonHolder(
        HTML("<span class="hidden">✓ Saved data</span>"),
        Submit('save', 'Save')
    )

- **MultiField**: It wraps fields in a ``<div>`` with a label on top. When there are errors in the form submission it renders them in a list instead of each one surrounding the field::

    MultiField("Text for the label {{ username }}",
        'form_field_1',
        'form_field_2'
    )

Bootstrap Layout objects
~~~~~~~~~~~~~~~~~~~~~~~~

This ones live in module ``crispy_forms.bootstrap``.

- **FormActions**: It wraps fields in a ``<div class="form-actions">``. This is a bootstrap layout object to wrapp form's submit buttons::

    FormActions(
        Submit('save', 'save', css_class="btn-primary")
    )

- **AppendedText**: It renders a bootstrap appended text input. The first parameter is the name of the field to add appended text to, then the appended text which can be HTML like. There is an optional parameter ``active``, by default set to ``False``, that you can set to a boolean to render appended text active::

    AppendedText('field_name', 'appended text to show')
    AppendedText('field_name', 'appended text to show', active=True)

- **PrependedText**: It renders a bootstrap prepended text input. The first parameter is the name of the field to add prepended text to, then the prepended text which can be HTML like. There is an optional parameter ``active``, by default set to ``False``, that you can set to a boolean to render prepended text active::

    PrependedText('field_name', '<b>Prepended text</b> to show')


Overriding layout objects templates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The mentioned set of :ref:`layout objects` has been thoroughly designed to be flexible, standard compatible and support Django form features. Every Layout object is associated to a different template that lives in ``templates/{{ TEMPLATE_PACK_NAME }}/layout/`` directory.

Some advanced users may want to use their own templates, to adapt the layout objects to their use or necessities. There are three ways to override the template that a layout object uses.

- **Globally**: You override the template of the layout object, for all instances of that layout object you use::

    from crispy_forms.layout import Div
    Div.template = 'my_div_template.html'

- **Individually**: You can override the template for a specific layout object in a layout::

    Layout(
        Div(
            'field1',
            'field2',
            template = 'my_div_template.html'
        )
    )

- **Overriding templates directory**: This means copying the templates directory into your project and overriding the templates editing them.

Overriding project templates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You need to differentiate between layout objects' templates and django-crispy-forms templates. There are some templates that live in ``templates/{{ TEMPLATE_PACK_NAME }}`` that define the form/formset structure, how a field or errors are rendered, etc. They add very little logic and are pretty much basic wrappers for the rest of django-crispy-forms power.

You can overwrite the templates that django-crispy-forms comes geared with using your own. If you have a template pack based on a CSS library, submit it so more people can benefit from it.

.. _`django-uni-form-contrib`: https://github.com/kennethlove/django-uni-form-contrib
.. _`Bootstrap`: https://github.com/twitter/bootstrap

Creating your own layout objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :ref:`layout objects` bundled with django-crispy-forms are a set of the most seen components that build a form. You will probably be able to do anything you need combining them. Anyway, you may want to create your own components, for doing that, you will need a good grasp of django-crispy-forms. Every layout object must have a method called ``render``. Its prototype should be::

    def render(self, form, form_style, context):

The official layout objects live in ``layout.py`` and ``bootstrap.py``, you may want to have a look at them to fully understand how to proceed. But in general terms, a layout object is a template rendered with some parameters passed.

If you come up with a good idea and design a layout object you think others could benefit from, please open an issue or send a pull request, so django-crispy-forms gets better.


Inheriting layouts
~~~~~~~~~~~~~~~~~~

Imagine you have several forms that share a big chunk of the same layout. There is a way you can create a ``Layout``, reuse and extend it in an easy way. You can have a ``Layout`` as a component of another ``Layout``, let's see an example::

    common_layout = Layout(
        MultiField("User data",
            'username',
            'lastname',
            'age'
        )
    )

    example_layout = Layout(
        common_layout,
        Div(
            'favorite_food',
            'favorite_bread',
            css_id = 'favorite-stuff'
        )
    )

    example_layout2 = Layout(
        common_layout,
        Div(
            'professional_interests',
            'job_description',
        )
    )

We have defined a ``common_layout`` that is used as a base for two different layouts: ``example_layout`` and ``example_layout2``, which means that those two layouts will start the same way and then extend the layout in different ways.
