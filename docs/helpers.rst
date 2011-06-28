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
    
In the appropriate form class, create a method (or better yet, a property) or instantiate the form helper class and include a form helper in the response context::

    class MyForm(forms.Form):
    
        @property
        def helper(self):
            """ We call this as a method/property so we don't make the form helper a singleton. """
        
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
            return helper
        
Now include use it in my_template.html::

    {% load uni_form_tags %}

    {% uni_form form form.helper %}

What you'll get is the form rendered as HTML with awesome bits. Specifically...

 * Opening and closing form tags::
    
    <form method="POST" action="/awesome/form/action/" 
        class="uniForm awesomeness" id="form-100">
        ...
    </form>
    
 * Django's CSRF controls::
 
    <div style="display:none">
        <input type="hidden" name="csrfmiddlewaretoken" 
            value="82ee0b84f9a10b211dfad61427ad1f76">
    </div> 
 
 * Submit and Reset Buttons::

    <div class="buttonHolder">

        <input type="submit" name="submit" value="Submit" 
            class="submit submitButton" id="submit-id-submit">

        <input type="reset" name="reset" value="Reset" 
            class="reset resetButton" id="reset-id-reset">

    </div>

Adding form helpers directly to forms 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to attach a form helper to a form, you have to make certain you don't accidentally create a singleton. Therefore, your best bet is to create the form helper inside a form method::

    # in forms.py
    from uni_form import helpers
    
    class MyForm(forms.Form):
    
        title = forms.CharField(_("Title"))
        
        @property
        def helper(self):
            """ Called as a property so we are certain the helper is not a singleton. """        
            helper = helpers.FormHelper()
            submit = helpers.Submit('submit','Submit')
            helper.add_input(submit)
            return helper

Now you can do something simple like this inside your template::

    {% load uni_form_tags %}

    {% uni_form form form.helper %}

    
Adding a layout to your form class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Uniform helpers can use layout objects. A layout can consist of fieldsets, rows, columns, HTML and fields. A simple Example::

    from django import forms

    from uni_form.helpers import FormHelper, Submit, Reset
    from uni_form.helpers import Layout, Fieldset, Row, HTML

    class LayoutTestForm(forms.Form):

        is_company = forms.CharField(label="company", required=False,
            widget=forms.CheckboxInput())    
        email = forms.CharField(label="email", max_length=30, required=True, 
            widget=forms.TextInput())        
        password1 = forms.CharField(label="password", max_length=30, 
            required=True, widget=forms.PasswordInput())
        password2 = forms.CharField(label="re-enter password", max_length=30,   
            required=True, widget=forms.PasswordInput())    
        first_name = forms.CharField(label="first name", max_length=30, 
            required=True, widget=forms.TextInput())        
        last_name = forms.CharField(label="last name", max_length=30, 
            required=True, widget=forms.TextInput())            

        @property
        def helper(self):
            """ Called as a property so we are certain the helper is not a singleton. """

            helper = FormHelper()

            # Create some HTML that you want in the page.
            # Yes, in real life your CSS would be cached, 
            #   but this is just a simple example.
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

            return helper

Now add the following to your template::

    {% load uni_form_tags %}
    
    {% uni_form form form.helper %}

This allows you to group fields in fieldsets, or rows or columns or add HTML between fields etc.
