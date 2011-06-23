.. django-uni-form documentation master file, created by
   sphinx-quickstart on Mon Mar  8 22:42:02 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

django-uni-form (django-uni-form)
=======================================

Django_ forms are easily rendered as tables,
paragraphs, and unordered lists. However, elegantly rendered div based forms
is something you have to do by hand. The purpose of this application is to
provide a simple filter that lets you quickly render forms in a div
format. Simple forms are easily rendered by the `as_uni_form` filter.

Via the `as_uni_form` filter::

    {% load uni_form_tags %}
    
    <form action="" method="POST" class="uniForm">
        {{ form|as_uni_form }} 
    </form>

And yet, django-uni-form does much more! By providing sophisticated layout controls you write in pure Python you can determine the layout and add buttons and controls to the forms with a minimum of HTML. This is done via the :ref:`form helpers` API. This way you can do stuff like::

    # In the form
    from uni_form.helpers import FormHelper, Submit, Reset
    
    class MyForm(forms.Form): # or class MyForm(forms.ModelForm)
    
        @property
        def helper(self):
            form = MyForm()
            helper = FormHelper()
            submit = Submit('search','search this site')
            helper.add_input(submit)
            helper.form_action = 'my-url-name-defined-in-url-conf'
            helper.form_method = 'GET' # Only GET and POST are legal
            return helper
    
    # In the template
    {% load uni_form_tags %}
    {% uni_form form form.helper %}
        
.. note:: Obviously, the excellent `Uni-form`_ has been selected as the base model for the design of the forms.

**Installation and Usage**

.. toctree::
    :maxdepth: 2

    install
    concepts
    usage
    helpers
    customization
    api_helpers
    api_templatetags    
   
**Help**

.. toctree::
    :maxdepth: 2

    faq
    contributors    
    changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _Django: http://djangoproject.com
.. _`Uni-form`: http://sprawsm.com/uni-form
