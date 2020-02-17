.. _`Form Helper`:

===========
Form Helper
===========

The getting started section gives an overview of the helper. This section explains more detailed features of the helper including the various attributes that can be set to help configure your form. 

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

    <form action="{% url 'submit_survey' %}" class="uniForm" method="post">
        {% crispy first_form %}
        {% crispy second_form %}
    </form>

You can read a list of :ref:`helper attributes` and what they are for.


Change '*' required fields
~~~~~~~~~~~~~~~~~~~~~~~~~~

If you don't like the use of ``*`` (asterisk) to denote required fields you have two options:

* Asterisks have an ``asteriskField`` class set. So you can hide it using CSS rule::

    .asteriskField {
        display: none;
    }

* Override ``field.html`` template with a custom one.


Make crispy-forms fail loud
~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default when crispy-forms encounters errors, it fails silently, logs them and continues working if possible. A settings variable called ``CRISPY_FAIL_SILENTLY`` has been added so that you can control this behavior. If you want to raise exceptions instead of logging, telling you what’s going on when you are developing in debug mode, you can set it to::

    CRISPY_FAIL_SILENTLY = not DEBUG


Change crispy-forms <input> default classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Django fields generate default classes, crispy-forms handles these and adds other classes for compatibility with CSS frameworks.

For example a ``CharField`` generates an ``<input class="textinput" ...``. But in uni form we need the class to be ``textInput`` (with capital 'I'), so crispy-forms leaves it like ``<input class="textinput textInput"...``. All official template packs are handled automatically, but maybe you are integrating a new CSS framework, or your company's custom one, with crispy-forms and need to change the default conversions. For this you need to use a settings variable called ``CRISPY_CLASS_CONVERTERS``, expected to be a Python dictionary::

    CRISPY_CLASS_CONVERTERS = {'textinput': "textinput inputtext"}

For example this setting would generate ``<input class"textinput inputtext" ...``. The key of the dictionary ``textinput`` is the Django's default class, the value is what you want it to be substituted with, in this case we are keeping ``textinput``.


Render a form within Python code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes, it might be useful to render a form using crispy-forms within Python code, like a Django view, for that there is a nice helper ``render_crispy_form``. The prototype of the method is ``render_crispy_form(form, helper=None, context=None)``. You can use it like this. Remember to pass your CSRF token to the helper method using the context dictionary if you want the rendered form to be able to submit.


AJAX validation recipe
~~~~~~~~~~~~~~~~~~~~~~

One easy way to validate a crispy-form through AJAX and re-render the resulting form errors if any is to set up a view, that validates the form and renders its html using ``render_crispy_form`` to finally return this html to the client AJAX request. Let's see an example.

Our server side code could be::

    from crispy_forms.utils import render_crispy_form

    @json_view
    def save_example_form(request):
        form = ExampleForm(request.POST or None)
        if form.is_valid():
            # You could actually save through AJAX and return a success code here
            form.save()
            return {'success': True}

        # RequestContext ensures CSRF token is placed in newly rendered form_html
        request_context = RequestContext(request)
        form_html = render_crispy_form(form, context=request_context)
        return {'success': False, 'form_html': form_html}

I'm using a jsonview decorator from `django-jsonview`_.

Note that in Django versions 1.8 and onwards, using ``RequestContext`` in this way will not work. Instead you can provide ``render_crispy_form`` with the necessary CSRF token with the following code::

    from django.template.context_processors import csrf
    ctx = {}
    ctx.update(csrf(request))
    form_html = render_crispy_form(form, context=ctx)

In our client side using jQuery would look like::

    var example_form = '#example-form';

    $.ajax({
        url: "{% url 'save_example_form' %}",
        type: "POST",
        data: $(example_form).serialize(),
        success: function(data) {
            if (!(data['success'])) {
                // Here we replace the form, for the
                $(example_form).replaceWith(data['form_html']);
            }
            else {
                // Here you can show the user a success message or do whatever you need
                $(example_form).find('.success-message').show();
            }
        },
        error: function () {
            $(example_form).find('.error-message').show()
        }
    });

Obviously, you can adjust this snippets to your needs, or class based views or favorite frontend library.

.. warning ::

    When replacing form html, you need to bind events using ``live`` or ``on`` jQuery method.

.. _`django-jsonview`: https://github.com/jsocol/django-jsonview

Bootstrap3 horizontal forms
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: images/bootstrap3_horizontal_form.jpg
   :align: center

The way you do horizontal forms in Bootstrap version 3 is setting some ``col-lg-X`` classes in labels and divs wrapping fields. This would mean a lot of hassle updating your layout objects for settings these classes, too much verbosity. Instead some ``FormHelper`` attributes have been added to help you easily achieve this. You will need to set only three attributes::

    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-8'
    helper.layout = Layout(
        'email',
        'password',
        'remember_me',
        StrictButton('Sign in', css_class='btn-default'),
    )

Of course you can set your widths as you like, it doesn't have to be exactly like this.

Bootstrap3 inline forms
~~~~~~~~~~~~~~~~~~~~~~~

.. image:: images/bootstrap3_inline_form.jpg
   :align: center

The way you do inline forms in Bootstrap version 3 is::

    helper.form_class = 'form-inline'
    helper.field_template = 'bootstrap3/layout/inline_field.html'
    helper.layout = Layout(
        'email',
        'password',
        'remember_me',
        StrictButton('Sign in', css_class='btn-default'),
    )

If you need to set attributes in a field, you have to use ``InlineField`` instead of ``Field``::

    from crispy_forms.bootstrap import InlineField

    helper.layout = Layout(
        InlineField('email', readonly=True),
        'password',
        [...]
    )



.. _`helper form attached`:

FormHelper with a form attached (Default layout)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Since version 1.2.0 ``FormHelper`` optionally can be passed an instance of a form. You would do it this way::

    from crispy_forms.helper import FormHelper

    class ExampleForm(forms.Form):
        def __init__(self, *args, **kwargs):
            super(ExampleForm, self).__init__(*args, **kwargs)
            self.helper = FormHelper(self)


When you do this crispy-forms builds a default layout using ``form.fields`` for you, so you don't have to manually list them all if your form is huge. If you later need to manipulate some bits of a big layout, using dynamic layouts is highly recommended, check :ref:`dynamic layouts`.

Also, now the helper is able to cross match the layout with the form instance, being able to search by widget type if you are using dynamic API.

.. _`helper attributes`:

Helper attributes you can set
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**template_pack**
    Allows you to set what template pack you want to use at ``FormHelper`` level. This is useful for example when a website needs to render different styling forms for different use cases, like desktop website vs smartphone website.

**template**
    When set allows you to render a form/formset using a custom template. Default template is at ``{{ TEMPLATE_PACK }}/[whole_uni_form.html|whole_uni_formset.html]``

**field_template**
    When set allows you to render a form/formset using a custom field template. Default template is at ``{{ TEMPLATE_PACK }}/field.html``.

**form_method = 'POST'**
    Specifies form method attribute. You can see it to ‘POST’ or ‘GET’. Defaults to ‘POST’

**form_action**
    Applied to the form action attribute. Can be a named url in your URLconf that can be executed via the {% url %} template tag. Example: ‘show_my_profile’. In your URLconf you could have something like::

        url(r'^show/profile/$', 'show_my_profile_view', name='show_my_profile')

    You can also point it to a URL ‘/whatever/blabla/’.

    Sometimes you may want to add arguments to the URL, for that you will have to do in your view::

        from django.urls import reverse
        form.helper.form_action = reverse('url_name', args=[event.id])
        form.helper.form_action = reverse('url_name', kwargs={'book_id': book.id})

**attrs**
    Added in 1.2.0, a dictionary to set any kind of form attributes. Underscores in keys are translated into hyphens. The recommended way when you need to set several form attributes in order to keep your helper tidy::

        ``{'id': 'form-id', 'data_id': '/whatever'}``
        <form id="form-id" data-id="/whatever" ...>

**form_id**
    Specifies form DOM id attribute. If no id provided then no id attribute is created on the form.

**form_class**
    String containing separated CSS classes to be applied to form class attribute. The form will always have by default ‘uniForm’ class.

**form_tag = True**
    It specifies if ``<form></form>`` tags should be rendered when using a Layout. If set to ``False`` it renders the form without the ``<form></form>`` tags. Defaults to ``True``.

**disable_csrf = False**
    Disable CSRF token, when done, crispy-forms won't use ``{% csrf_token %}`` tag. This is useful when rendering several forms using ``{% crispy %}`` tag and ``form_tag = False`` csrf_token gets rendered several times.

**form_error_title**
    If you are rendering a form using ``{% crispy %}`` tag and it has ``non_field_errors`` to display, they are rendered in a div. You can set the title of the div with this attribute. Example: “Form Errors”.

**formset_error_title**
    If you are rendering a formset using ``{% crispy %}`` tag and it has ``non_form_errors`` to display, they are rendered in a div. You can set the title of the div with this attribute. Example: “Formset Errors”.

**form_style = 'default'**
    Helper attribute for uni_form template pack. Uni-form has two different form styles built-in. You can choose which one to use, setting this variable to ``default`` or ``inline``.

**form_show_errors = True**
    Default set to ``True``. It decides whether to render or not form errors. If set to ``False``, form.errors will not be visible even if they happen. You have to manually render them customizing your template. This allows you to customize error output.

**render_unmentioned_fields = False**
    By default django-crispy-forms renders the layout specified if it exists strictly, which means it only renders what the layout mentions, unless your form has ``Meta.fields`` and ``Meta.exclude`` defined, in that case it uses them. If you want to render unmentioned fields (all form fields), for example if you are worried about forgetting mentioning them you have to set this property to ``True``. It defaults to ``False``.

**render_hidden_fields = False**
    By default django-crispy-forms renders the layout specified if it exists strictly. Sometimes you might be interested in rendering all form's hidden fields no matter if they are mentioned or not. It defaults to ``False``.

**render_required_fields = False**
    By default django-crispy-forms renders the layout specified if it exists strictly. Sometimes you might be interested in rendering all form's required fields no matter if they are mentioned or not. It defaults to ``False``.

**include_media = True**
    By default django-crispy-forms renders all form media for you within the form. If you want to render form media yourself manually outside the form, set this to ``False``. If you want to globally prevent rendering of form media, override the FormHelper class with this setting modified. It defaults to ``True``.


Bootstrap Helper attributes
~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are currently some helper attributes that only have functionality for a specific template pack. This doesn't necessarily mean that they won't be supported for other template packs in the future.

**help_text_inline = False**
    Sets whether help texts should be rendered inline or block. If set to ``True`` help texts will be rendered using ``help-inline`` class, otherwise using ``help-block``. By default text messages are rendered in block mode.

**error_text_inline = True**
    Sets whether to render error messages inline or block. If set to ``True`` errors will be rendered using ``help-inline`` class, otherwise using ``help-block``. By default error messages are rendered in inline mode.

**html5_required = False**
    When set to ``True`` all required fields inputs will be rendered with HTML5 ``required=required`` attribute.

**form_show_labels = True**
    Default set to ``True``. Determines whether or not to render the form's field labels.


Bootstrap 3 Helper attributes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All previous, ``bootstrap`` (version 2) attributes are also settable in bootstrap 3 template pack ``FormHelpers``. Here are listed the ones, that are only available in ``bootstrap3`` template pack:

**label_class = ''**
    Default set to ``''``. This class will be applied to every label, this is very useful to do horizontal forms. Set it for example like this ``label_class = col-lg-2``.

**field_class = ''**
    Default set to ``''``. This class will be applied to every div ``controls`` wrapping a field. This is useful for doing horizontal forms. Set it for example like this ``field_class = col-lg-8``.


Bootstrap 4 Helper attributes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All previous, ``bootstrap`` (version 2 and 3) attributes are also settable in bootstrap 4 template pack ``FormHelpers``. Here are listed the ones, that are only available in ``bootstrap4`` template pack:

**use_custom_control = True**
    Enables the `optional UI customization <https://getbootstrap.com/docs/4.3/components/forms/#custom-forms>`_ of the template pack for radio, checkbox and file field (non clearable only). Useful when you already have customization based on the default interpretation of the template pack. Setting to ``False`` results in the `standard bootstrap <https://getbootstrap.com/docs/4.3/components/forms/#checkboxes-and-radios>`_ classes being applied for radio and checkbox, and Django rendering for file field. See table below for examples. 
    
    The file field requires `additional JS <https://www.w3schools.com/bootstrap4/bootstrap_forms_custom.asp#myFile>`_ to enable its functionality, it is provided within the template pack as vanilla JS. 
    
    Defaults to ``True``.

.. |checkbox| image:: images/checkbox.png
   :width: 300px
   :align: middle
.. |customcheckbox| image:: images/custom_checkbox.png
   :width: 300px
   :align: middle
.. |radio| image:: images/radio.png    
   :width: 300px
   :align: middle
.. |customradio| image:: images/custom_radio.png
   :width: 300px
   :align: middle
.. |file| image:: images/file_field.png    
   :height: 60px
   :align: middle
.. |customfile| image:: images/custom_file_field.png
   :width: 300px
   :align: middle

+------------------+------------------+
|     Standard     |     Optional     |
+------------------+------------------+
| |checkbox|       | |customcheckbox| |
+------------------+------------------+
|  |radio|         | |customradio|    |
+------------------+------------------+
|  |file|          | |customfile|     |
+------------------+------------------+

Custom Helper attributes
~~~~~~~~~~~~~~~~~~~~~~~~

Maybe you would like ``FormHelper`` to do some extra thing that is not currently supported or maybe you have a very specific use case. The good thing is that you can add extra attributes and crispy-forms will automagically inject them within template context. Let's see an example, to make things clear.

We want some forms to have uppercase labels, and for that we would like to set a helper attribute name ``labels_uppercase`` to ``True`` or ``False``. So we go and set in our helper::

    helper.labels_uppercase = True

What will happen is crispy-forms will inject a Django template variable named ``{{ labels_uppercase }}`` with its corresponding value within its templates, including ``field.html``, which is the template in charge of rendering a field when using crispy-forms. So we can go into that template and customize it. We will need to get familiar with it, but it's quite easy to follow; in the end it's just a Django template.

When we find where labels get rendered, this chunk of code to be more precise::

    {% if field.label and not field|is_checkbox and form_show_labels %}
        <label for="{{ field.id_for_label }}" class="control-label {% if field.field.required %}requiredField{% endif %}">
            {{ field.label|safe }}{% if field.field.required %}<span class="asteriskField">*</span>{% endif %}
        </label>
    {% endif %}

The line that we would change wold end up like this::

    {% if not labels_uppercase %}{{ field.label|safe }}{% else %}{{ field.label|safe|upper }}{% endif %}{% if field.field.required %}

Now we only need to override field template, for that you may want to check section :ref:`override templates`.

.. warning ::

    Be careful, depending on what you aim to do, sometimes using dynamic layouts is a better option, check section :ref:`dynamic layouts`.
