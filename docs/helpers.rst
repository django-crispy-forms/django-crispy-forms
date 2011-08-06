.. _`form helpers`:

==============
Form Helpers
==============

django-uni-form implements a class called `FormHelper` that defines the form rendering behavior. Helpers give you a way to control form attributes and its layout, doing this in a programatic way using Python. This way you touch HTML as little as possible, and all your logic stays in the forms and views files.

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
        
Let's see how helpers works step by step, with some examples explained. First you will need to import `FormHelper`::

    from uni_form.helper import FormHelper

Your helper can be a class level variable or an instance level variable, if you don't know what this means you might want to read the article "`Be careful how you use static variables in forms`_". As a rule of thumb, if you are not going to manipulate a form helper in your code, like in a view, you should be using a static helper, otherwise you should be using an instance level helper. In the next steps I will show you how to manipulate the form helper, so we will create an instance level helper. This is how you would do it::

    from uni_form.helper import FormHelper
    
    class ExampleForm(forms.Form):
        [...]
        def __init__(self, *args, **kwargs):
            self.helper = FormHelper()
            return super(ExampleForm, self).__init__(*args, **kwargs)

As you can see you need to override the constructor and call the base class constructor using `super`. This helper doesn't set any form attributes, so it's useless. Let's see how to set up some basic FormHelper attributes::

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

            self.helper.add_inputs(Submit('submit', 'Submit')
            return super(ExampleForm, self).__init__(*args, **kwargs)

Note that we are importing here a class called `Submit` that is a layout object. We will see what layout objects are in detail later on, for now on let's just say that this adds a submit button to our form, so people can send their survey.

We've also done some helper magic. `FormHelper` has a list of attributes that can be set, that affect mainly form attributes. Our form will have as DOM id `id-exampleForm`, it will have as DOM CSS class `blueForms`, it will use http `POST` to send information and its action will be set to `reverse(submit_survey)`. 

Let's how you render a form with a helper using django-uni-form custom tags. First we need to load django-uni-form tags in the templates we use them: 

    {% load uni_form_tags %}

Supposing we have the form in the template context as `example_form`, we would render it doing:

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
    It specifies if `<form></form>` tags should be rendered when using a Layout. If set to False it renders the form without the `<form></form>` tags. Defaults to True.

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

You might be thinking that helpers are nice, but what if you need to change the way the form fields are rendered, answer is layouts. Django-uni-form defines another powerful class called `Layout`. You can create your `Layout` to define how the form fields should be rendered: order of the fields, wrap them in divs or other html structures with ids or classes set to whatever you want, add things in between, etc. And all that without writing a custom template, rather fully reusable without writing it twice.

A Layout is constructed by what I like to call layout objects, which can be thought of as form components. You assemble your layout using those. For the time being, your choices are: ButtonHolder, Button, Div, Row, Column, Fieldset, HTML, Hidden, MultiField, Reset and Submit.

All these components are explained in helper API docs. What you need to know now about them is that every component renders a different template. Let’s write a couple of different layouts for our form, continuing with our form class example (note that I’m not showing the full form again):

Let's add a layout to our helper::

    from uni_form.helper import FormHelper
    from uni_form.layout import Layout, Fieldset

    class ExampleForm(forms.Form):
        [...]
        def __init__(self, *args, **kwargs):
            self.helper = FormHelper()
            self.helper.layout = Layout(
                Fieldset(
                    'legend of the fieldset',
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

We will get the fields wrapped in a fieldset, the fields order will be: like_website, favorite_number, favorite_color, favorite_food and notes. We also get a Submit button wrapped in a `<div class="buttonHolder">` which uni-form CSS positions in a nice way. That button has its CSS class set to `button white`.

This is just the peak of the iceberg. Now imagine you want to add an explanation for what notes are, you can use `HTML` layout object::

    Layout(
        Fieldset(
            'legend of the fieldset',
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

This way you will get a message before the notes input. Note how you can wrap layout objects into other layout objects.


Creating your own layout objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    
Overriding layout objects templates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. _`Be careful how you use static variables in forms`: http://tothinkornottothink.com/post/7157151391/be-careful-how-you-use-static-variables-in-forms 
