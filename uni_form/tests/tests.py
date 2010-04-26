from django import forms
from django.conf import settings
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
        self.assertTrue('default.uni-form.css' in html)
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
        '''
        self.assertTrue('class="submit submitButton"' in html)
        self.assertTrue('id="submit-id-my-submit"' in html)        

        self.assertTrue('class="reset resetButton"' in html)
        self.assertTrue('id="reset-id-my-reset"' in html)        

        self.assertTrue('name="my-hidden"' in html)        

        self.assertTrue('class="button"' in html)
        self.assertTrue('id="button-id-my-button"' in html)        
        '''
    def test_uni_form_helper_form_attributes(self):
        

        template = get_template_from_string("""
            {% load uni_form_tags %}
            {% uni_form form form_helper %}
        """)        

        # First we build a standard form helper
        form_helper = FormHelper()    
        form_helper.form_id = 'this-form-rocks'
        form_helper.form_class = 'forms-that-rock'
        form_helper.form_method = 'GET'
    
        # now we render it
        c = Context({'form':TestForm(),'form_helper':form_helper})            
        html = template.render(c)        
        
        # Lets make sure everything loads right
        self.assertTrue("""<form""" in html)                
        self.assertTrue("""class="uniForm forms-that-rock" """ in html)
        self.assertTrue("""method="get" """ in html)
        self.assertTrue("""id="this-form-rocks">""" in html)        
        
        # now lets remove the form tag and render it again. All the True items above
        # should now be false because the form tag is removed.
        form_helper.form_tag = False
        c = Context({'form':TestForm(),'form_helper':form_helper})            
        html = template.render(c)        
        self.assertFalse("""<form""" in html)        
        self.assertFalse("""id="this-form-rocks">""" in html)                
        self.assertFalse("""class="uniForm forms-that-rock" """ in html)
        self.assertFalse("""method="get" """ in html)
        self.assertFalse("""id="this-form-rocks">""" in html)
        

    def test_csrf_token(self):
        is_old_django = getattr(settings, 'OLD_DJANGO', False) # TODO: remove when pre-CSRF token templatetags are no longer supported
        if not is_old_django: # TODO: remove when pre-CSRF token templatetags are no longer supported
            response = self.client.get('/more/csrf_token_test/')
            self.assertContains(response, "<input type='hidden' name='csrfmiddlewaretoken'")
