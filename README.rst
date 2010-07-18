=====================================
django-uni-form (django-uni-form)
=====================================

Django_ forms are easily rendered as tables,
paragraphs, and unordered lists. However, elegantly rendered div based forms
is something you have to do by hand. The purpose of this application is to
provide a simple tag and/or filter that lets you quickly render forms in a div
format.

`Uni-form`_ has been selected as the base model for the design of the forms.

**Warning:** django-uni-form 0.8 and higher renders django.form.field labels with the 'safe' filter. If you have user generated form field labels you should take this into consideration.

**Note:** django-uni-form 0.8 and higher lays out the HTML for the uni_form tag differently than previous versions. The errorMsg div is now outside the fieldset as it should be.

**Note:** django-uni-form 0.7 and higher breaks backwards compatibility with previous versions of django-uni-form. All you have to do is update templates that call on the django-uni-form template tag from::

    {% load uni_form %}
    
To::

    {% load uni_form_tags %}

Installation
============

Dependencies
~~~~~~~~~~~~

 * JQuery

Installing django-uni-form
~~~~~~~~~~~~~~~~~~~~~~~~~~

Install into your python path using pip or easy_install::

    pip install django-uni-form
    easy_install django-uni-form    
    
Add *'uni_form'* to your INSTALLED_APPS in settings.py::

    INSTALLED_APPS = (
        ...
        'uni_form',
        )
        
Depending on your setup, you may need to copy the media files to your local 
media folder::

    cp -r <location-of-django-uni-form>/uni_form/media/uni_form <directory-for-my-project's-media-files>
    
Displaying the media files
~~~~~~~~~~~~~~~~~~~~~~~~~~

First, make sure you're linking to a copy of jQuery.  It's recommended that you use the version hosted on Google's servers since the user's browser might already have it cached.  (You can get the url for the latest version of jQuery at http://scriptsrc.net/.)  But there are some cases in which you'll want to host jQuery yourself, such as if you're doing development offline::

    <script src="{{ MEDIA_URL }}js/jquery.js" type="text/javascript"></script>

Beyond jQuery, django-uni-form requires three media files.  You can see how we call them by looking in the templates/includes.html file. You can call those files in several ways.

1. The best way is probably to copy this HTML into your templates.  (This allows you to make use of django_compressor, a dead easy media compressor for Django that's also hosted here on github.)  Here's the HTML::

    <link rel="stylesheet" href="{{ MEDIA_URL }}uni_form/uni-form.css" type="text/css" />
    <link rel="stylesheet" href="{{ MEDIA_URL }}uni_form/default.uni-form.css" type="text/css" />
    <!-- note that there's also blue.uni-form.css and dark.uni-form.css available if you want to try changing things up -->
    <script src="{{ MEDIA_URL }}uni_form/uni-form.jquery.js" type="text/javascript"></script>

2. Another way is to use Django's built-in **includes** template tag::

    {% include "uni_form/includes.html" %}
    
3. A third way is to use the django-uni-form **uni_form_setup** template tag.  Note that you'll need some additional setup for this::

    {% uni_form_setup %}

If you want to take advantage of the uni_form_setup tag, then you'll need to make sure '*django.core.context_processors.request*' is in the  TEMPLATE_CONTEXT_PROCESSORS tuple in your settings.py file::

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'django.core.context_processors.request',
        )
        
Customizations on '*' required fields (optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you don't like the use of '*' (asterisk) to denote required fields you can simply overrride the django-uni-form field.html. In your Django project's templates directory create a new directory called `uni_form`. Copy the django-uni-form field.html file to that directory and make the desired changes. For example::

    cd ~/<my-projects>/<my-awesome-django-project>/templates/
    mkdir uni_form
    cd uni_form/
    cp <my-site-packages>/Django-uni-form/uni_form/templates/uni_form/field.html .
    
Now you could change the asterisk to any other character, an image icon, or whatever else you want.

Using Uni-Form strict fields
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

django-uni-form implements form fields in html differently than the standard Uni-Form. If you want to adhere to the strict definition of django-uni-form relplace the field.html file with field.strict.html. You can just follow these instructions::

    cd ~/<my-projects>/<my-awesome-django-project>/templates/
    mkdir uni_form
    cd uni_form/
    cp <my-site-packages>/Django-uni-form/uni_form/templates/field.strict.html field.html

----

Usage
=====

Using the django-uni-form filter (Easy and fun!)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Add ``{% load uni_form_tags %}`` to the template that calls your form.
2. Append your form call with the as_uni_form filter::

    {{ my_form|as_uni_form }}

3. Add the class of 'uniForm' to your form. Example::

    <form action="" method="post" class="uniForm">

4. Refresh and enjoy!

Using the django-uni-form templatetag in your view (Intermediate)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. In your views.py add the following after field definitions::

    from django.shortcuts import render_to_response
    
    from uni_form.helpers import FormHelper, Submit, Reset
    from my_project.forms.MyForm
    
    def my_view(request):
    
        # Create the form
        form = MyForm() 
    
        # create a formHelper
        helper = FormHelper()
        
        # Add in a class and id
        helper.form_id = 'this-form-rocks'
        helper.form_class = 'search'
        
        # add in a submit and reset button
        submit = Submit('search','search this site')
        helper.add_input(submit)
        reset = Reset('reset','reset button')                
        helper.add_input(reset)
        
        # create the response dictionary
        response_dictionary = {'form':form, 'helper': helper}
        
        return render_to_response('my_template.html', response_dictionary)
        
2. In your template do the following::

    {% load uni_form_tags %}
    
    {% uni_form form helper %}

Using the django-uni-form templatetag in your form class (Intermediate)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. In your form class add the following after field definitions::

    from uni_form.helpers import FormHelper, Submit, Reset

    class MyForm(forms.Form):
        title = forms.CharField(label=_("Title"), max_length=30, widget=forms.TextInput())

        # Attach a formHelper to your forms class.
        helper = FormHelper()
        
        # Add in a class and id
        helper.form_id = 'this-form-rocks'
        helper.form_class = 'search'
        
        # add in a submit and reset button
        submit = Submit('search','search this site')
        helper.add_input(submit)
        reset = Reset('reset','reset button')                
        helper.add_input(reset)
        
2. In your template do the following::

    {% load uni_form_tags %}
    {% with form.helper as helper %}
        {% uni_form form helper %}
    {% endwith %}
    
Using the django-uni-form templatetag to change action/method (Intermediate)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. In your form class add the following after field definitions::

    from uni_form.helpers import FormHelper, Submit

    class MyForm(forms.Form):
        title = forms.CharField(label=_("Title"), max_length=30, widget=forms.TextInput())

        # Attach a formHelper to your forms class.
        helper = FormHelper()
        
        # Change the form and method
        helper.form_action = 'my-url-name-defined-in-url-conf'
        helper.form_method = 'GET' # Only GET and POST are legal
        
        # add in a submit and reset button
        submit = Submit('search','search this site')
        helper.add_input(submit)
        
2. In your template do the following::

    {% load uni_form_tags %}
    {% with form.helper as helper %}
        {% uni_form form helper %}
    {% endwith %}



Adding a layout to your form class (Intermediate)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Uniform helpers can use layout objects. A layout can consist of fieldsets, rows, columns, HTML and fields. A simple Example::

    from django import forms
    
    from uni_form.helpers import FormHelper, Submit, Reset
    from uni_form.helpers import Layout, Fieldset, Row, HTML
	
    class LayoutTestForm(forms.Form):

        is_company = forms.CharField(label="company", required=False, widget=forms.CheckboxInput())    
        email = forms.CharField(label="email", max_length=30, required=True, widget=forms.TextInput())        
        password1 = forms.CharField(label="password", max_length=30, required=True, widget=forms.PasswordInput())
        password2 = forms.CharField(label="re-enter password", max_length=30, required=True, widget=forms.PasswordInput())    
        first_name = forms.CharField(label="first name", max_length=30, required=True, widget=forms.TextInput())        
        last_name = forms.CharField(label="last name", max_length=30, required=True, widget=forms.TextInput())            
    
        # Attach a formHelper to your forms class.
        helper = FormHelper()

        # Create some HTML that you want in the page.
        # Yes, in real life your CSS would be cached, but this is just a simple example.
        style = """
        <style>
            .formRow {
                color: red;
            }
        </style>
    
        """
        # create the layout object
        layout = Layout(
                        # first fieldset shows the company
                        Fieldset('', 'is_company'),
                    
                        # second fieldset shows the contact info
                        Fieldset('Contact details',
                                HTML(style),
                                'email',
                                Row('password1','password2'),
                                'first_name',
                                'last_name',
                                 )
                        )

        helper.add_layout(layout)
                      
        submit = Submit('add','Add this contact')
        helper.add_input(submit)
        
Then, just like in the previous example, add the following to your template::

    {% load uni_form_tags %}
    {% with form.helper as helper %}
        {% uni_form form helper %}
    {% endwith %}
           

This allows you to group fields in fieldsets, or rows or columns or add HTML between fields etc.

.. _Django: http://djangoproject.com
.. _`Uni-form`: http://sprawsm.com/uni-form
