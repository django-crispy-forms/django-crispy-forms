.. _`form helpers`:

==============
Form Helpers
==============

What Helpers give you is the ability to add attributes, controls, and layout 
components to a form in Python. This way you touch HTML as little as possible, and all your logic is in the forms and views file.

Fundamentals
~~~~~~~~~~~~

This is easier to demonstrate via example then explain.

Import the uni_form helpers::

    from uni_form import helpers
    
In the appropriate view function (or Class Based View), instantiate the form helper class and include a form helper in the response context::

    def my_view(request):
    
        # create the form
        form = SearchForm()
        
        # instantiate the form helper object
        helper = helpers.FormHelper()

        # add in some input controls (a.k.a. buttons)
        submit = helpers.Submit('submit','Submit')
        helper.add_input(submit)
        reset = helpers.Reset('reset','Reset')
        helper.add_input(reset)
        
        # define the form action
        helper.form_action = reverse('awesome-form-action')
        helper.form_method = 'POST'
        helper.form_class = 'awesomeness'
        helper.form_id = 'form-100'
        
        # create the response dictionary
        response_dictionary = {'form':form, 'helper': helper}        
        return render_to_response('my_template.html', response_dictionary)        

Now include it in my_template.html::

    {% load uni_form_tags %}

    {% uni_form form helper %}

What you'll get is the form rendered as HTML with awesome bits. Specifically...

 * Opening and closing form tags::
    
    <form method="POST" action="/awesome/form/action/" class="uniForm awesomeness" id="form-100">
        ...
    </form>
    
 * Django's CSRF controls::
 
    <div style="display:none">
        <input type="hidden" name="csrfmiddlewaretoken" 
            value="82ee0b84f9a10b211dfad61427ad1f76">
    </div> 
 
 * Submit and Reset Buttons::

    <div class="buttonHolder">

        <input type="submit" name="submit" value="Submit" class="submit submitButton" id="submit-id-submit">

        <input type="reset" name="reset" value="Reset" class="reset resetButton" id="reset-id-reset">

    </div>

Adding form helpers directly to forms 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to attach a form helper to a form, you have to make certain you don't accidentally create a singleton. Therefore, your best bet is to create the form helper inside a form method::

    # in forms.py
    from uni_form import helpers
    
    class MyForm(forms.Form):
    
        title = forms.CharField(_("Title"))
        
        def get_helper(self):
            helper = helpers.FormHelper()
            submit = helpers.Submit('submit','Submit')
            helper.add_input(submit)
            return helper

Now you can do something simple like this inside your template::

    {% load uni_form_tags %}

    {% uni_form form form.get_helper %}

    
Layouts
~~~~~~~

TODO - here goes describing how layouts go.
