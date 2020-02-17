===============
Getting Started
===============

There are two key ways which django-crispy-forms can be implemented in your template files to make your forms crispy.

The first approach is using ``|crispy`` filter. This is simple to implement, think of it as the built-in methods: ``as_table``, ``as_ul`` and ``as_p``. However, as with the built-in methods you cannot tune up the output. 

The second approach uses a custom tag ``{% crispy %}`` which allows much more customisation of your form. It will change how you do forms in Django.

crispy filter
=============

Crispy filter lets you render a form or formset using django-crispy-forms elegantly div based fields. Let's see a usage example::

    {% load crispy_forms_tags %}
    
    <form method="post" class="uniForm">
        {{ my_formset|crispy }}
    </form>

1. Add ``{% load crispy_forms_tags %}`` to the template.
2. Append the ``|crispy`` filter to your form or formset context variable.
3. If you are using ``uni_form`` template pack, don't forget to add the class 'uniForm' to your form.
4. Refresh and enjoy!


{% crispy %} tag with forms
===========================

django-crispy-forms implements a class called ``FormHelper`` that defines the form rendering behavior. Helpers give you a way to control form attributes and its layout, doing this in a programmatic way using Python. This way you write as little HTML as possible, and all your logic stays in the forms and views files.

Fundamentals
~~~~~~~~~~~~

For the rest of this document we will use the following example form for showing how to use a helper. This form is in charge of gathering some user information::

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
            label = "What is your favorite food?",
            max_length = 80,
            required = True,
        )

        favorite_color = forms.CharField(
            label = "What is your favorite color?",
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

    from crispy_forms.helper import FormHelper

Your helper can be a class level variable or an instance level variable, if you don't know what this means you might want to read the article "`Be careful how you use static variables in forms`_". As a rule of thumb, if you are not going to manipulate a `FormHelper` in your code, like in a view, you should be using a static helper, otherwise you should be using an instance level helper. If you still don't understand the subtle differences between both, use an instance level helper, because you won't end up suffering side effects. As in the next steps I will show you how to manipulate the form helper, so we will create an instance level helper. This is how you would do it::

    from crispy_forms.helper import FormHelper

    class ExampleForm(forms.Form):
        [...]
        def __init__(self, *args, **kwargs):
            super(ExampleForm, self).__init__(*args, **kwargs)
            self.helper = FormHelper()

As you can see you need to call the base class constructor using ``super`` and override the constructor. This helper doesn't set any form attributes, so it's useless. Let's see how to set up some basic `FormHelper` attributes::

    from crispy_forms.helper import FormHelper
    from crispy_forms.layout import Submit

    class ExampleForm(forms.Form):
        [...]
        def __init__(self, *args, **kwargs):
            super(ExampleForm, self).__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_id = 'id-exampleForm'
            self.helper.form_class = 'blueForms'
            self.helper.form_method = 'post'
            self.helper.form_action = 'submit_survey'

            self.helper.add_input(Submit('submit', 'Submit'))

Note that we are importing a class called ``Submit`` that is a layout object. We will see what layout objects are in detail later on, for now on let's just say that this adds a submit button to our form, so people can send their survey.

We've also done some helper magic. ``FormHelper`` has a list of attributes that can be set, that affect mainly form attributes. Our form will have as DOM id ``id-exampleForm``, it will have as DOM CSS class ``blueForms``, it will use http ``POST`` to send information and its action will be set to ``reverse(submit_survey)``.

Let's see how to render the form in a template. Supposing we have the form in the template context as ``example_form``, we would render it doing::

    {% load crispy_forms_tags %}
    {% crispy example_form example_form.helper %}

Notice that the ``{% crispy %}`` tags expects two parameters: first the form variable and then the helper. In this case we use the ``FormHelper`` attached to the form, but you could also create a ``FormHelper`` instance and pass it as a context variable. Most of the time, you will want to use the helper attached. Note that if you name your ``FormHelper`` attribute ``helper`` you will only need to do::

    {% crispy form %}

This is exactly the html that you would get::

    <form action="/submit/survey/" class="uniForm blueForms" method="post" id="id-exampleForm">
        <div style='display:none'>
            <input type="hidden" name="csrfmiddlewaretoken" value="a643fab735d5ce6377ff456e73c4b1af" />
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
                <input id="id_favorite_food" class="textinput textInput" type="text" name="favorite_food" maxlength="80" required="required" />
            </div>
            <div id="div_id_favorite_color" class="ctrlHolder">
                <label for="id_favorite_color" class="requiredField">What is you favorite color?<span class="asteriskField">*</span></label>
                <input id="id_favorite_color" class="textinput textInput" type="text" name="favorite_color" maxlength="80" required="required" />
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
        <input type="hidden" name="csrfmiddlewaretoken" value="a643fab735d5ce6377ff456e73c4b1af" />
    </div>

 * Submit button::

    <div class="buttonHolder">
        <input type="submit" name="submit" value="Submit" class="submit submitButton" id="submit-id-submit" />
    </div>

.. _`Be careful how you use static variables in forms`: http://tothinkornottothink.com/post/7157151391/be-careful-how-you-use-static-variables-in-forms

