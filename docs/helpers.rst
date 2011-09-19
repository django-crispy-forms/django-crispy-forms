.. _`form helpers`:

==================
{% uni_form %} tag
==================

django-uni-form implements a class called ``FormHelper`` that defines the form rendering behavior. Helpers give you a way to control form attributes and its layout, doing this in a programatic way using Python. This way you touch HTML as little as possible, and all your logic stays in the forms and views files.

For using this you will need to use django-uni-form ``{% uni_form %}`` tag.


Fundamentals
~~~~~~~~~~~~

From now onwards we will use the following form to exemplify how to use a helper. This form is in charge of gathering some user information::

    class ExampleForm(forms.Form):
        like_website = forms.TypedChoiceField(
            label = "Do you like this website?",
            choices = ((1, "Yes"), (0, "No")),
            coerce = lambda x: bool(int(x)),
            widget = forms.RadioSelect,
            initial = '1',
            required = True,
        )

        favorite_food = forms.CharField(
            label = "What is you favorite food?",
            max_length = 80,
            required = True,
        )

        favorite_color = forms.CharField(
            label = "What is you favorite color?",
            max_length = 80,
            required = True,
        )

        favorite_number = forms.IntegerField(
            label = "Favorite number",
            required = False,
        )

        notes = forms.CharField(
            label = "Additional notes or feedback",
            required = False,
        )
        
Let's see how helpers works step by step, with some examples explained. First you will need to import ``FormHelper``::

    from uni_form.helper import FormHelper

Your helper can be a class level variable or an instance level variable, if you don't know what this means you might want to read the article "`Be careful how you use static variables in forms`_". As a rule of thumb, if you are not going to manipulate a form helper in your code, like in a view, you should be using a static helper, otherwise you should be using an instance level helper. If you still don't understand the subtle differences between both, use an instance level helper, because you won't end up suffering side effects. As in the next steps I will show you how to manipulate the form helper, so we will create an instance level helper. This is how you would do it::

    from uni_form.helper import FormHelper
    
    class ExampleForm(forms.Form):
        [...]
        def __init__(self, *args, **kwargs):
            self.helper = FormHelper()
            return super(ExampleForm, self).__init__(*args, **kwargs)

As you can see you need to override the constructor and call the base class constructor using ``super``. This helper doesn't set any form attributes, so it's useless. Let's see how to set up some basic FormHelper attributes::

    from uni_form.helper import FormHelper
    from uni_form.layout import Submit

    class ExampleForm(forms.Form):
        [...]
        def __init__(self, *args, **kwargs):
            self.helper = FormHelper()
            self.helper.form_id = 'id-exampleForm'
            self.helper.form_class = 'blueForms'
            self.helper.form_method = 'post'
            self.helper.form_action = 'submit_survey'

            self.helper.add_input(Submit('submit', 'Submit')
            return super(ExampleForm, self).__init__(*args, **kwargs)

Note that we are importing here a class called ``Submit`` that is a layout object. We will see what layout objects are in detail later on, for now on let's just say that this adds a submit button to our form, so people can send their survey.

We've also done some helper magic. ``FormHelper`` has a list of attributes that can be set, that affect mainly form attributes. Our form will have as DOM id ``id-exampleForm``, it will have as DOM CSS class ``blueForms``, it will use http ``POST`` to send information and its action will be set to ``reverse(submit_survey)``. 

Let's how you render a form with a helper using django-uni-form custom tags. First we need to load django-uni-form tags in the templates we use them: 

    {% load uni_form_tags %}

Supposing we have the form in the template context as ``example_form``, we would render it doing:

    {% uni_form example_form example_form.helper %}

This is exactly the html that you would get::

    <form action="/submit/survey/" class="uniForm blueForms" method="post" id="id-exampleForm">
        <div style='display:none'>
            <input type='hidden' name='csrfmiddlewaretoken' value='a643fab735d5ce6377ff456e73c4b1af' />
        </div>
        <fieldset>
            <legend></legend>
            <div id="div_id_like_website" class="ctrlHolder">
                <label for="id_like_website" class="requiredField">¿Do you like this website?<span class="asteriskField">*</span></label>
                <ul>
                    <li><label for="id_like_website_0"><input checked="checked" name="like_website" value="1" id="id_like_website_0" type="radio" class="radioselect" /> Yes</label></li>
                    <li><label for="id_like_website_1"><input value="0" type="radio" class="radioselect" name="like_website" id="id_like_website_1" /> No</label></li>
                </ul>
            </div>
            <div id="div_id_favorite_food" class="ctrlHolder">
                <label for="id_favorite_food" class="requiredField">What is you favorite food?<span class="asteriskField">*</span></label>
                <input id="id_favorite_food" class="textinput textInput" type="text" name="favorite_food" maxlength="80" />
            </div>
            <div id="div_id_favorite_color" class="ctrlHolder">
                <label for="id_favorite_color" class="requiredField">What is you favorite color?<span class="asteriskField">*</span></label>
                <input id="id_favorite_color" class="textinput textInput" type="text" name="favorite_color" maxlength="80" />
            </div>
            <div id="div_id_favorite_number" class="ctrlHolder">
                <label for="id_favorite_number">Favorite number</label>
                <input id="id_favorite_number" type="text" name="favorite_number" class="textinput textInput" />
            </div>
            <div id="div_id_notes" class="ctrlHolder">
                <label for="id_notes">Additional notes or feedback</label>
                <input id="id_notes" type="text" name="notes" class="textinput textInput" />
            </div>
        </fieldset>
        <div class="buttonHolder">
            <input type="submit" name="submit" value="Submit" class="submit submitButton" id="submit-id-submit" />
        </div>
    </form>

What you'll get is the form rendered as HTML with awesome bits. Specifically...

 * Opening and closing form tags, with id, class, action and method set as in the helper::
    
    <form action="/submit/survey/" class="uniForm blueForms" method="post" id="id-exampleForm">
        [...]
    </form>
    
 * Django's CSRF controls::
 
    <div style='display:none'>
        <input type='hidden' name='csrfmiddlewaretoken' value='a643fab735d5ce6377ff456e73c4b1af' />
    </div>
 
 * Submit button::

    <div class="buttonHolder">
        <input type="submit" name="submit" value="Submit" class="submit submitButton" id="submit-id-submit" />
    </div>


Manipulating a helper in a view
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's see how we could change any helper property in a view::

    @login_required()
    def inbox(request, template_name):
        example_form = ExampleForm()
        redirect_url = request.GET.get('next')

        # Form handling logic
        [...]
 
        if redirect_url is not None:
            example_form.helper.form_action = reverse('submit_survey') + '?next=' + redirectUrl
        
        return render_to_response(template_name, {'example_form': example_form}, context_instance=RequestContext(request))

We are changing ``form_action`` helper property in case the view was called with a ``next`` GET parameter.


Rendering several forms with helpers 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Often we get asked, how do you render two or more forms, with their respective helpers, using ``{% uni_form %}`` tags, without having ``<form>`` tags rendered twice? Easy, you need to set ``form_tag`` helper property to False in every helper::

    self.helper.form_tag = False

 Then you will have to write a little of html code surrounding the forms::

    <form action="{% url submit_survey %}" class="uniForm" method="post">
        {% uni_form first_form first_form.helper %}
        {% uni_form second_form second_form.helper %}
    </form>

You can read a list of :ref:`helper attributes` and what they are for.


Make django-uni-form fail loud
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default when django-uni-form encounters errors, it fails silently, logs them and continue working if possible. A settings variable called ``UNIFORM_FAIL_SILENTLY`` has been added so that you can control this behavior. If you want django-uni-form to raise errors instead of logging, telling you what’s going on when you are developing in debug mode, you can set it to::

    UNIFORM_FAIL_SILENTLY = not DEBUG


Rendering a formset
~~~~~~~~~~~~~~~~~~~

``{% uni_form %}`` tag supports formsets rendering too. All the previous stated things apply to formsets the same way. Imagine you create a formset using the previous ``ExampleForm`` form::

    from django.forms.models import formset_factory

    ExampleFormset = formset_factory(ExampleForm, extra = 3)
    example_formset = ExampleFormset()

This is how you would render the formset::

    {% uni_form formset formset.form.helper %}

Note that you can still use a helper (in this case we are using the helper of the form used for building the formset). The main difference here is that helper attributes are applied to the form structure, while the layout is applied to the formset’s forms. Rendering formsets injects some extra context in the layout rendering so that you can do things like::

    HTML("{% if forloop.first %}Message displayed only in the first form of a formset forms list{% endif %}",
    Fielset("Item {{ forloop.counter }}", 'field-1', [...])

Basically you can access a ``forloop`` Django node, as if you were rendering your formsets forms using a for loop.


.. _`helper attributes`:
Helper attributes you can set
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

form_method
    Specifies form method attribute. You can see it to ‘POST’ or ‘GET’. Defaults to ‘POST’

form_action
    Applied to the form action attribute. Can be a named url in your URLconf that can be executed via the {% url %} template tag. Example: ‘show_my_profile’. In your URLconf you could have something like::

        url(r'^show/profile/$', 'show_my_profile_view', name = 'show_my_profile')

    You can also point it to a URL ‘/whatever/blabla/’.

form_id
    Specifies form DOM id attribute. If no id provided then no id attribute is created on the form.

form_class
    String containing separated CSS clases to be applied to form class attribute. The form will always have by default ‘uniForm’ class.

form_tag
    It specifies if ``<form></form>`` tags should be rendered when using a Layout. If set to False it renders the form without the ``<form></form>`` tags. Defaults to True.

form_error_title
    If you are rendering a form using {% uni_form %} tag and it has non_field_errors to display, they are rendered in a div. You can set the title of the div with this attribute. Example: “Form Errors”.

formset_error_title 
    If you are rendering a formset using {% uni_form %} tag and it has non_form_errors to display, they are rendered in a div. You can set the title of the div with this attribute. Example: “Formset Errors”.

form_style
    If you are using uni-form CSS, it has two different form styles built-in. You can choose which one to use, setting this variable to “default” or “inline”.


=======
Layouts 
=======

Fundamentals
~~~~~~~~~~~~

You might be thinking that helpers are nice, but what if you need to change the way the form fields are rendered, answer is layouts. Django-uni-form defines another powerful class called ``Layout``. You can create your ``Layout`` to define how the form fields should be rendered: order of the fields, wrap them in divs or other structures, add html, set ids or classes to whatever you want, etc. And all that without writing a custom template, rather fully reusable without writing it twice. Then just attach the layout to a helper, layouts are optional, but probably the most powerful thing django-uni-form has to offer.

A Layout is constructed by layout objects, which can be thought of as form components. You assemble your layout using those. For the time being, your choices are: ``ButtonHolder``, ``Button``, ``Div``, ``Row``, ``Column``, ``Fieldset``, ``HTML``, ``Hidden``, ``MultiField``, ``Reset`` and ``Submit``.

All these components are explained later in :ref:`layout objects`. What you need to know now about them is that every component renders a different template. Let’s write a couple of different layouts for our form, continuing with our form class example (note that the full form is not shown again):

Let's add a layout to our helper::

    from uni_form.helper import FormHelper
    from uni_form.layout import Layout, Fieldset

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
                )
                ButtonHolder(
                    Submit('submit', 'Submit', css_class='button white')
                )
            )
            return super(ExampleForm, self).__init__(*args, **kwargs)

When we render the form now using::

    {% load uni_form_tags %}
    {% uni_form example_form example_form.helper %}

We will get the fields wrapped in a fieldset, whose legend will be set to 'first arg is the legend of the fieldset'. The fields order will be: ``like_website``, ``favorite_number``, ``favorite_color``, ``favorite_food`` and ``notes``. We also get a submit button wrapped in a ``<div class="buttonHolder">`` which uni-form CSS positions in a nice way. That button has its CSS class set to ``button white``.

This is just the peak of the iceberg. Now imagine you want to add an explanation for what notes are, you can use ``HTML`` layout object::

    Layout(
        Fieldset(
            'Tell us your favorite stuff {{ username }}',
            'like_website',
            'favorite_number',
            'favorite_color',
            'favorite_food',
            HTML("""
                <p>We use notes to get better, <strong>please help us {{ username }}</strong></p> 
            """)
            'notes'
        )
    )

As you notice the fieldset legend is context aware and you can write it as if it were a chunk of a template where the form will be rendered. the ``HTML`` object will add a message before the notes input and it's also context aware. Note how you can wrap layout objects into other layout objects. Layout objects ``Fieldset``, ``Div``, ``Row``, ``Column``, ``MultiField`` and ``ButtonHolder`` can hold other Layout objects within. Let's do an alternative layout for the same form::

    Layout(
        MultiField(
            'Tell us your favorite stuff {{ username }}',
            Div(
                'like_website',
                'favorite_number',
                css_id = 'special-fields'
            )
            'favorite_color',
            'favorite_food',
            'notes'
        )
    )

This time we are using a ``MultiField``, which is a layout object that as a general rule can be used in the same places as ``Fieldset``. The main difference is that this renders all the fields wrapped in a div and when there are errors in the form submission, they are shown in a list instead of each one surrounding the field. Sometimes the best way to see what layout objects do, is just try them and play with them a little bit.


.. _`layout objects`:
Layout objects
~~~~~~~~~~~~~~

Let's see an example of every layout object in use, to understand what parameters each one expects.

- **Div**: It wraps fields in a div::

    Div('form_field_1', 'form_field_2', 'form_field_3', ...)

- **Row and Column**: They are child classes of ``Div``, which wrap fields in divs with CSS classes already set to ``formRow`` and ``formColumn`` respectively. These are maintained for backwards compatibility, but uni-form CSS rules doesn't format this in any way. It is recommended to use ``Div`` instead for new projects::

    Row('form_field_1', 'form_field_2', 'form_field_3', ...)
    Column('form_field_1', 'form_field_2', 'form_field_3', ...)

- **HTML**: A very powerful layout object, to render pure html code. You can write as a Django template and it has access to the whole context of the page where the form is being rendered::

    HTML("{% if success %} <p>Operation was successful</p> {% endif %}")

- **Submit**: Used to create a submit button. First parameter is the ``name`` attribute of the button, second parameter is the ``value`` attribute::

    Submit('search', 'SEARCH')

Renders to::
    
    <input type="submit" name="search" value="SEARCH" class="submit submitButton" id="submit-id-search" />

- **Hidden**: Used to create a hidden input::

    Hidden('name', 'value')

- **Button**: Creates a button::
    
    Button('name', 'value')
    
- **Reset**: Used to create a reset input::

    reset = Reset('name', 'value')

- **ButtonHolder**: It wraps fields in a ``<div class=”buttonHolder”>``, which uni-form positions in a nice way. This is where you should put visible layout objects that render to form inputs like ``Submit`` or ``Button``::

    ButtonHolder(
        HTML("<span class="hidden">✓ Saved data</span>"),
        Submit('save', 'Save')
    )

- **Fieldset**: It wraps fields in a ``<fieldset>``. The first parameter is the text for the fieldset legend, as we've said it behaves like a Django template::

    Fieldset("Text for the legend {{ username }}",
        'form_field_1',
        'form_field_2'
    )

- **MultiField**: It wraps fields in a div with a label on top. When there are errors in the form submission it renders them in a list instead of each one surrounding the field::

    Fieldset("Text for the label {{ username }}",
        'form_field_1',
        'form_field_2'
    )

All this layout objects, can have their DOM id or class set using named arguments ``css_id`` and ``css_class``::

    Div('form_field_1', 'form_field_2', 'form_field_3', css_id = 'magic-div-1', css = 'magic-divs')
    Submit('save', 'Save', css_id = 'submit-save', css_class = 'button white')


Overriding layout objects templates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Django-uni-form provides a set of :ref:`layout objects`, that have been thoroughly designed to be flexible, standard compatible and support Django form features. Every Layout object is associated to a different template that lives in ``templates/uni_form/layout/`` directory.

Some advanced users may want to use their own templates, to adapt the layout objects to their use or necessities. There are two ways to override the template that a layout object uses. 

- **Globally**: You override the template of the layout object, for all instances of that layout object you use::

    from uni_form.layout import Div
    Div.template = 'my_div_template.html'

- **Individually**: You can override the template for a specific layout object in a layout::

    Layout(
        Div(
            'field1',
            'field2',
            template = 'my_div_template.html'
        )
    )

Overriding project templates 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You need to differentiate between layout objects templates and django-uni-form templates. There are some templates that live in ``templates/uni_form`` that define the form/formset structure, how a field or errors are rendered, etc. They add very little logic and are pretty much basic wrappers for the rest of django-uni-form power. This were thought to be used with uni-form, although they work without it, as they simply add some CSS classes that don't cause any trouble.

You can overwrite the templates that django-uni-form comes geared with using your own. As it was mentioned, you are free to not use uni-form anymore. Kenneth Love has created `django-uni-form-contrib`_ for adding more template packs to django-uni-form you can easily plug in, such as a `Bootstrap`_ pack. If you have a template pack based on a CSS library, submit it so more people can benefit from it.

.. _`django-uni-form-contrib`: https://github.com/kennethlove/django-uni-form-contrib
.. _`Bootstrap`: https://github.com/twitter/bootstrap

Creating your own layout objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :ref:`layout objects` bundled with django-uni-form are a set of the most seen components that build a form. You will probably be able to do anything you need combining them. Anyway, you may want to create your own components, for doing that, you will need a good grasp of django-uni-form. Every layout object must have a method called ``render``. Its prototype should be::

    def render(self, form, form_style, context):

The official layout objects live in ``layout.py``, you may want to have a look at them to fully understand how to proceed. But in general terms, a layout object is a template rendered with some parameters passed.

If you come up with a good idea and design a layout object you think others could benefit from, please open an issue or send us a pull request, so we can make django-uni-form better.


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


Updating layouts on the go
~~~~~~~~~~~~~~~~~~~~~~~~~~

Layouts can be changed, adapted and generated dynamically. At the moment, ``Layout`` doesn't have an API for handling this, so as in Django forms you will need to access inner attribute ``fields``. Main difference compared to Django forms is that ``fields`` is a Python list and not a dictionary. To sum up all layout objects and ``Layout`` itself hold a ``fields`` list that you can tamper. You can access the layout attached to a helper with::

    form.helper.layout

This is how you would add one layout object at the end of the layout::

    layout.fields.append(HTML("<p>whatever</p>"))

This is how you would add several layout objects::

    layout.fields.extend([
        HTML("<p>whatever</p>"),
        Div('add_field_on_the_go')
    ])

This is how you would replace a layout object::

    layout.fields[2] = HTML("<p>whatever</p>")

This is how you would delete the second layout object::

    layout.fields.pop(1)

This is how you would insert a layout object in the second position::

    layout.fields.insert(1, HTML("<p>whatever</p>"))

.. Warning ::

    Remember always that if you are going to manipulate a helper or layout in a view or any part of your code, you better use an instance level variable.


.. _`Be careful how you use static variables in forms`: http://tothinkornottothink.com/post/7157151391/be-careful-how-you-use-static-variables-in-forms 
