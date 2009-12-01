=====================================
django-uni-form (Django Uni-Form)
=====================================

Django_ forms are easily rendered as tables,
paragraphs, and unordered lists. However, elegantly rendered div based forms
is something you have to do by hand. The purpose of this application is to
provide a simple tag and/or filter that lets you quickly render forms in a div
format.

`Uni-form`_ has been selected as the base model for the design of the forms.

**Note:** Django Uni-Form 0.7 breaks backwards compatibility with previous versions of Django Uni-Form. See ``Updating legacy Django Uni-Form to 0.7``. All you have to do is update templates that call on the Django Uni-Form template tag from::

    {% load uni_form %}
    
To::

    {% load uni_form_tags %}

Installation
============

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

    cp -r <location-of-django-uni-form>/uni_form/media/uni_form/uni-form-generic.css <my-project>/media/uni_form/uni-form-generic.css
    cp -r <location-of-django-uni-form>/uni_form/media/uni_form/uni-form.css <my-project>/media/uni_form/uni-form.css
    cp -r <location-of-django-uni-form>/uni_form/media/uni_form/uni-form.jquery.js <my-project>/media/uni_form/uni-form.jquery.js    
    
Displaying the media files
~~~~~~~~~~~~~~~~~~~~~~~~~~

Django Uni-Form requires three media files.  You can see how we call them by looking in the templates/includes.html file. You can call those files in several ways:

1. Manually by copying the HTML into your own templates::

    <link rel="stylesheet" href="{{ MEDIA_URL }}uni_form/uni-form-generic.css" type="text/css" />
    <link rel="stylesheet" href="{{ MEDIA_URL }}uni_form/uni-form.css" type="text/css" />
    <script src="{{ MEDIA_URL }}uni_form/uni-form.jquery.js" type="text/javascript"></script>

2. Via use of the Django **includes** built-in template tag.

    {% include "uni_form/includes.html" %}
    
3. With some additional setup described below, via use of the Django Uni-Form **uni_form_setup** template tag.

    {% uni_form_setup %}

If you want to take advantage of the uni_form_setup tag, then you'll need to make sure '*django.core.context_processors.request*' is in the  TEMPLATE_CONTEXT_PROCESSORS tuple in your settings.py file::

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'django.core.context_processors.request',
        )
        
Customizations on '*' required fields (optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you don't like the use of '*' (asterisk) to denote required fields you can simply overrride the Django Uni-Form field.html. In your Django project's templates directory create a new directory called `uni_form`. Copy the Django Uni-Form field.html file to that directory and make the desired changes. For example::

    cd ~/<my-projects>/<my-awesome-django-project>/templates/
    mkdir uni_form
    cd uni_form/
    cp <my-site-packages>/Django-uni-form/uni_form/templates/field.html .
    
Now you could change the asterisk to any other character, an image icon, or whatever else you want.

Using Uni-Form strict fields
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Django Uni-Form implements form fields in html differently than the standard Uni-Form. If you want to adhere to the strict definition of Django Uni-Form relplace the field.html file with field.strict.html. You can just follow these instructions::

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
