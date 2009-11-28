from django import forms
from django.template import Context, Template
from django.template.loader import get_template_from_string
from django.test import TestCase

from uni_form.helpers import FormHelper, Submit, Reset, Hidden, Button

class TestForm(forms.Form):
    
    is_company = forms.CharField(label="company", required=False, widget=forms.CheckboxInput())
    email = forms.CharField(label="email", max_length=30, required=True, widget=forms.TextInput())
    password1 = forms.CharField(label="password", max_length=30, required=True, widget=forms.PasswordInput())
    password2 = forms.CharField(label="re-enter password", max_length=30, required=True, widget=forms.PasswordInput())
    first_name = forms.CharField(label="first name", max_length=30, required=True, widget=forms.TextInput())
    last_name = forms.CharField(label="last name", max_length=30, required=True, widget=forms.TextInput())


class TestBasicFunctionalityTags(TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_as_uni_form(self):
        
        # build the context
        c = Context({'form':TestForm()})
        
        # Simple form templare
        template = get_template_from_string("""
{% load uni_form_tags %}
{{ form|as_uni_form }}
        """)
        
        # render the form template
        html = template.render(c)
        
        self.assertTrue("<td>" not in html)
        self.assertTrue("id_is_company" in html)
    
    def test_uni_form_setup(self):
        
        c = Context()
        template = get_template_from_string("""
{% load uni_form_tags %}
{% uni_form_setup %}
        """)
        html = template.render(c)
        
        # Just look for file names because locations and names can change.
        self.assertTrue('uni-form-generic.css' in html)
        self.assertTrue('uni-form.css' in html)
        self.assertTrue('uni-form.jquery.js' in html)
        
class TestFormHelpers(TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass    
    
    def test_uni_form_helper_inputs(self):
        
        form_helper = FormHelper()
        submit  = Submit('my-submit', 'Submit')
        reset   = Reset('my-reset', 'Reset')
        hidden  = Hidden('my-hidden', 'Hidden')
        button  = Button('my-button', 'Button')
        form_helper.add_input(submit)
        form_helper.add_input(reset)
        form_helper.add_input(hidden)
        form_helper.add_input(button)
        
        c = Context({'form':TestForm(),'form_helper':form_helper})        
        
        template = get_template_from_string("""
{% load uni_form_tags %}
{% uni_form form form_helper %}
        """)
        html = template.render(c)
        
        self.assertTrue('class="submit submitButton"' in html)
        self.assertTrue('id="submit-id-my-submit"' in html)        

        self.assertTrue('class="reset resetButton"' in html)
        self.assertTrue('id="reset-id-my-reset"' in html)        

        self.assertTrue('name="my-hidden"' in html)        

        self.assertTrue('class="button"' in html)
        self.assertTrue('id="button-id-my-button"' in html)        

    def test_uni_form_helper_generic_attributes(self):
        
        form_helper = FormHelper()    
        form_helper.form_id = 'this-form-rocks'
        form_helper.form_class = 'forms-that-rock'
        form_helper.form_method = 'GET'
    
        c = Context({'form':TestForm(),'form_helper':form_helper})            
        template = get_template_from_string("""
{% load uni_form_tags %}
{% uni_form form form_helper %}
        """)
        html = template.render(c)        

        good_response = """<form action="" class="uniForm forms-that-rock" method="POST" id="this-form-rocks" >"""
        
        self.assertTrue('<form action="" class="uniForm forms-that-rock" method="GET" id="this-form-rocks" >' in html)