from django import forms
from django.template.loader import render_to_string

from uni_form.helpers import FormHelper, Submit, Reset

from uni_form.helpers import Layout, Fieldset, Column, Row, HTML


class TestForm(forms.Form):
    
    character_field = forms.CharField(label="Character Field", help_text="I am help text", max_length=30, required=True, widget=forms.TextInput())
    url_field = forms.URLField(label='URL field', verify_exists=False, max_length=100, required=True, widget=forms.TextInput())
    textarea_field = forms.CharField(label='Textareafield', required=True, widget=forms.Textarea())
    hidden_field = forms.CharField(label='textarea_field', required=True, widget=forms.HiddenInput())
    file_field  = forms.FileField(label="File Field",required=False)



class HelperTestForm(TestForm):
    
    # Attach a formHelper to your forms class.
    helper = FormHelper()
    
    # Add in a class and id
    helper.form_id = 'this-form-rocks'
    helper.form_class = 'search'
    
    # add in a submit and reset button
    submit = Submit('enter','enter some data')
    helper.add_input(submit)
    reset = Reset('reset','reset button')
    helper.add_input(reset)



class LayoutTestForm(forms.Form):

    is_company = forms.CharField(label="company", required=False, widget=forms.CheckboxInput())    
    email = forms.CharField(label="email", max_length=30, required=True, widget=forms.TextInput())        
    password1 = forms.CharField(label="password", max_length=30, required=True, widget=forms.PasswordInput())
    password2 = forms.CharField(label="re-enter password", max_length=30, required=True, widget=forms.PasswordInput())    
    first_name = forms.CharField(label="first name", max_length=30, required=True, widget=forms.TextInput())        
    last_name = forms.CharField(label="last name", max_length=30, required=True, widget=forms.TextInput())            
    
    # Attach a formHelper to your forms class.
    helper = FormHelper()

    # create some HTML that you want in the page
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

class MessageResponseForm(forms.Form):
    
    character_field = forms.CharField(label="Character Field", help_text="I am help text", max_length=30, required=True, widget=forms.TextInput())

    def clean(self):
        cleaned_data = self.cleaned_data
        raise forms.ValidationError("This is a forced error")
        return cleaned_data
