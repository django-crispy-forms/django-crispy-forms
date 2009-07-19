from django import forms

from uni_form.helpers import FormHelper, Submit, Reset


class TestForm(forms.Form):
    
    character_field = forms.CharField(label="Character Field", max_length=30, required=True, widget=forms.TextInput())    
    url_field = forms.URLField(label='URL field', verify_exists=False, max_length=100, required=True, widget=forms.TextInput())    
    textarea_field = forms.CharField(label='textarea_field', required=True, widget=forms.Textarea())
    
    


class HelperTestForm(TestForm):

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
    
