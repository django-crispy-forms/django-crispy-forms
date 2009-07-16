=====================================
django-uni-form (Django Uni-Form)
=====================================

Django_ forms are easily rendered as tables,
paragraphs, and unordered lists. However, elegantly rendered div based forms
is something you have to do by hand. The purpose of this application is to
provide a simple tag and/or filter that lets you quickly render forms in a div
format.

`Uni-form`_ has been selected as the base model for the design of the forms.

Installing django-uni-form
============================
1. Install as uni_form in your Django apps directory.
2. Copy the site_media files in uni_form to your project site_media directory.
    uni-form-generic.css
    uni-form.css
    uni-form.jquery.js
3. Add 'uni_form' to INSTALLED_APPS in settings.py.


Using the django-uni-form filter (Easy and fun!)
=================================================
1. Add ``{% load uni_form %}`` to the template that calls your form.
2. Append your form call with the as_uni_form filter::

    {{ my_form|as_uni_form }}

3. Add the class of 'uniForm' to your form. Example::

    <form action="" method="post" class="uniForm">

4. Refresh and enjoy!

Using the django-uni-form templatetag in your view (Intermediate)
====================================================================
1. In your form class add the following after field definitions::

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

    {% load uni_form %}
    
    {% uni_form form helper %}



Using the django-uni-form templatetag in your form class (Intermediate)
========================================================================
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

    {% load uni_form %}
    {% with form.helper as helper %}
        {% uni_form form helper %}
    {% endwith %}


Adding a layout to your form
============================

Uniform helper can have a layout. A layout can consist of fieldsets, rows, columns, HTML and fields.
A complex Example::

	help_text = render_to_string("example/help_text.html")
	layout = Layout(Fieldset(_('Basic Settings'),
                             'title',
                             'type',
                             'available_date',
                    		),
                    Fieldset(_('Overview'),
                             Column(Fieldset(_('Object address'),
                                             Row('address', 'street_number'),
                                             Row('zip', 'city'),
                                             'area',
                                            ),
                                    Fieldset(_("Next public transport"),
                                             'train_station',
                                             Row('tram_station','tram_number'),
                                             Row('bus_station','bus_number'),
                                             ),
                                    ),
                             Column("is_for_rent",
                                    Fieldset(_("Rent"),
                                             'rent-price',
                                             ),
                                    Fieldset(_("Sell"),
                                             'buy_price',
                                             ),
                                    Fieldset(_("Measurements"),
                                             'floor_space',
                                             'room_height',
                                             'construction_year',
                                             ),
                             ),
                    Fieldset(_('Additional Function'),
                             HTML('<p class="tip">%s</p>' % unicode(help_text)),
                             'features',
                             ),
                    Fieldset(_("Description"),
                             "description")
                    )
    helper.add_layout(layout)

This allows you to group fields in fieldsets, or rows or columns or add HTML between fields etc.


.. _Django: http://djangoproject.com
.. _`Uni-form`: http://sprawsm.com/uni-form