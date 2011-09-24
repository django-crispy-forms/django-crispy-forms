.. django-uni-form documentation master file, created by
   sphinx-quickstart on Mon Mar  8 22:42:02 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

django-uni-form
===============

Django_ forms are easily rendered as tables, paragraphs, and unordered lists. However, elegantly rendered div based forms is something you have to do by hand. The purpose of this application is to provide a tag and filter that lets you quickly render forms in a div format while providing an enormous amount of capability to configure and control the rendered HTML. 

It comes geared with a filter called ``|as_uni_form`` and a tag called ``{% uni_form %}``. 

You can use the filter to render your forms using elegantly div based fields::

    {% load uni_form_tags %}
    
    <form action="" method="POST" class="uniForm">
        {{ form|as_uni_form }} 
    </form>

And yet, django-uni-form does much more! By providing a form helper and sophisticated layout handling easily attachable to a form, you can control form rendering behavior and create a form layout in pure Python with a minimum of HTML, thus controling things like order of the fields, wrap them in divs or other structures, add html, set DOM ids or classes to whatever you want, adding inputs, etc. This is done via the :ref:`form helpers`. This way you can do stuff like::

    from uni_form.helper import FormHelper
    from uni_form.layout import Layout, Div, ButtonHolder, Submit
    
    class MyForm(forms.Form):   # or class MyForm(forms.ModelForm)
        form_field_1 = forms.CharField(...)

        def __init__(self, *arg, **kwargs):
            self.helper = FormHelper()
            self.helper.form_action = 'my-url-name-defined-in-url-conf'
            self.helper.form_method = 'GET'

            self.helper.layout = Layout(
                Div(
                    'form_field_4',
                    'form_field_1',
                )
                Div(
                    'form_field_2',
                    'form_field_3',
                )
                ButtonHolder(
                    Submit('save', 'Save', css_class='button white')
                )
            )
            return super(MyForm, self).__init__(*args, **kwargs)

You can render an instance of `MyForm` using this helper and layout adding this code to a template, you wont::
    
    {% load uni_form_tags %}
    {% uni_form my_form my_form.helper %}
            
.. note:: Obviously, the excellent `Uni-form`_ has been selected as the base model for the design of the forms.

**User Guide**
This part of the documentation, which is mostly prose, begins with some background information about django-uni-form, then focuses on step-by-step instructions for getting the most out of it.

.. toctree::
    :maxdepth: 2

    install
    concepts
    usage
    helpers
    customization
    faq
    contributors
    changelog

**API documentation**
If you are looking for information on a specific function, class or method, this part of the documentation is for you.

.. toctree::
    :maxdepth: 2
    
    api_helpers
    api_layout
    api_templatetags
   
**Developer Guide**
Think this is awesome and want to make it better? Read our contribution_ page, make it better, and we'll add you to the contributors_ list!

.. toctree::
    :maxdepth: 2

    contributing

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _contribution: contributing.html
.. _contributors: contributors.html
.. _Django: http://djangoproject.com
.. _`Uni-form`: http://sprawsm.com/uni-form
