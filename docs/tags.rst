.. _`form helpers`:

================
{% crispy %} tag
================

django-crispy-forms implements a class called ``FormHelper`` that defines the form rendering behavior. Helpers give you a way to control form attributes and its layout, doing this in a programatic way using Python. This way you write as little HTML as possible, and all your logic stays in the forms and views files.

Fundamentals
~~~~~~~~~~~~

For the rest of this document we will use the following example form of how to use a helper. This form is in charge of gathering some user information::

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

    from crispy_forms.helper import FormHelper

Your helper can be a class level variable or an instance level variable, if you don't know what this means you might want to read the article "`Be careful how you use static variables in forms`_". As a rule of thumb, if you are not going to manipulate a `FormHelper` in your code, like in a view, you should be using a static helper, otherwise you should be using an instance level helper. If you still don't understand the subtle differences between both, use an instance level helper, because you won't end up suffering side effects. As in the next steps I will show you how to manipulate the form helper, so we will create an instance level helper. This is how you would do it::

    from crispy_forms.helper import FormHelper
    
    class ExampleForm(forms.Form):
        [...]
        def __init__(self, *args, **kwargs):
            self.helper = FormHelper()
            super(ExampleForm, self).__init__(*args, **kwargs)

As you can see you need to override the constructor and call the base class constructor using ``super``. This helper doesn't set any form attributes, so it's useless. Let's see how to set up some basic `FormHelper` attributes::

    from crispy_forms.helper import FormHelper
    from crispy_forms.layout import Submit

    class ExampleForm(forms.Form):
        [...]
        def __init__(self, *args, **kwargs):
            self.helper = FormHelper()
            self.helper.form_id = 'id-exampleForm'
            self.helper.form_class = 'blueForms'
            self.helper.form_method = 'post'
            self.helper.form_action = 'submit_survey'

            self.helper.add_input(Submit('submit', 'Submit'))
            super(ExampleForm, self).__init__(*args, **kwargs)

Note that we are importing a class called ``Submit`` that is a layout object. We will see what layout objects are in detail later on, for now on let's just say that this adds a submit button to our form, so people can send their survey.

We've also done some helper magic. ``FormHelper`` has a list of attributes that can be set, that effect mainly form attributes. Our form will have as DOM id ``id-exampleForm``, it will have as DOM CSS class ``blueForms``, it will use http ``POST`` to send information and its action will be set to ``reverse(submit_survey)``. 

Let's see how to render the form in a template. Supposing we have the form in the template context as ``example_form``, we would render it doing::

    {% load crispy_forms_tags %}
    {% crispy example_form example_form.helper %}

Notice that the ``{% crispy %}`` tags expects two parameters: first the form variable and then the helper. In this case we use the ``FormHelper`` attached to the form, but you could also create a ``FormHelper`` instance and pass it as a context variable. Most of the time, you will want to use the helper attached. Note that if you name your ``FormHelper`` attribute ``helper`` you will only need to do::

    {% crispy form %}

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

Often we get asked: "How do you render two or more forms, with their respective helpers, using ``{% crispy %}`` tag, without having ``<form>`` tags rendered twice?" Easy, you need to set ``form_tag`` helper property to ``False`` in every helper::

    self.helper.form_tag = False

Then you will have to write a little of html code surrounding the forms::

    <form action="{% url submit_survey %}" class="uniForm" method="post">
        {% crispy first_form %}
        {% crispy second_form %}
    </form>

You can read a list of :ref:`helper attributes` and what they are for.


Make django-crispy-forms fail loud
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default when django-crispy-forms encounters errors, it fails silently, logs them and continues working if possible. A settings variable called ``CRISPY_FAIL_SILENTLY`` has been added so that you can control this behavior. If you want to raise exceptions instead of logging, telling you what’s going on when you are developing in debug mode, you can set it to::

    CRISPY_FAIL_SILENTLY = not DEBUG


Rendering formsets
~~~~~~~~~~~~~~~~~~

``{% crispy %}`` tag supports formsets rendering too. All the previous stated things apply to formsets the same way. Imagine you create a formset using the previous ``ExampleForm`` form::

    from django.forms.models import formset_factory

    ExampleFormset = formset_factory(ExampleForm, extra = 3)
    example_formset = ExampleFormset()

This is how you would render the formset. Note that this time you need to specify the helper explicitly::

    {% crispy formset formset.form.helper %}

Note that you can still use a helper (in this case we are using the helper of the form used for building the formset). The main difference here is that helper attributes are applied to the form structure, while the layout is applied to the formset’s forms. Rendering formsets injects some extra context in the layout rendering so that you can do things like::

    HTML("{% if forloop.first %}Message displayed only in the first form of a formset forms list{% endif %}",
    Fielset("Item {{ forloop.counter }}", 'field-1', [...])

Basically you can access a ``forloop`` Django node, as if you were rendering your formsets forms using a for loop.


.. _`helper attributes`:

Helper attributes you can set
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**form_method = 'POST'**
    Specifies form method attribute. You can see it to ‘POST’ or ‘GET’. Defaults to ‘POST’

**form_action**
    Applied to the form action attribute. Can be a named url in your URLconf that can be executed via the {% url %} template tag. Example: ‘show_my_profile’. In your URLconf you could have something like::

        url(r'^show/profile/$', 'show_my_profile_view', name = 'show_my_profile')

    You can also point it to a URL ‘/whatever/blabla/’.

**form_id**
    Specifies form DOM id attribute. If no id provided then no id attribute is created on the form.

**form_class**
    String containing separated CSS clases to be applied to form class attribute. The form will always have by default ‘uniForm’ class.

**form_tag = True**
    It specifies if ``<form></form>`` tags should be rendered when using a Layout. If set to ``False`` it renders the form without the ``<form></form>`` tags. Defaults to ``True``.

**form_error_title**
    If you are rendering a form using ``{% crispy %}`` tag and it has ``non_field_errors`` to display, they are rendered in a div. You can set the title of the div with this attribute. Example: “Form Errors”.

**formset_error_title**
    If you are rendering a formset using ``{% crispy %}`` tag and it has ``non_form_errors`` to display, they are rendered in a div. You can set the title of the div with this attribute. Example: “Formset Errors”.

**form_style = 'default'**
    Helper attribute for uni_form template pack. Uni-form has two different form styles built-in. You can choose which one to use, setting this variable to ``default`` or ``inline``.

**form_show_errors = True**
    Default set to ``True``. It decides wether to render or not form errors. If set to ``False``, form.errors will not be visible even if they happen. You have to manually render them customizing your template. This allows you to customize error output.

**render_unmentioned_fields = False**
    By default django-crispy-forms renders the layout specified if it exists strictly, which means it only renders what the layout mentions, unless your form has ``Meta.fields`` and ``Meta.exclude`` defined, in that case it uses them. If you want to render unmentioned fields in the layout, for example if you are worried about forgetting mentioning them you have to set this property to ``True``. It defaults to ``False``.

**help_text_inline = False**
    Use this helper attribute to set if help texts if you are using bootstrap template pack, should be rendered ``help-inline`` or using ``help-block``. By default ``help-block`` is used.


.. _`Be careful how you use static variables in forms`: http://tothinkornottothink.com/post/7157151391/be-careful-how-you-use-static-variables-in-forms
