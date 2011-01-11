from django import forms
from django.conf import settings
from django.template import Context, Template
from django.template.loader import get_template_from_string
from django.template.loader import render_to_string
from django.middleware.csrf import _get_new_csrf_key
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
        template = get_template_from_string(u"""
            {% load uni_form_tags %}
            {{ form|as_uni_form }}
        """)
        c = Context({'form': TestForm()})
        html = template.render(c)
        
        self.assertTrue("<td>" not in html)
        self.assertTrue("id_is_company" in html)
    
    def test_uni_form_setup(self):
        template = get_template_from_string("""
            {% load uni_form_tags %}
            {% uni_form_setup %}
        """)
        c = Context()
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
        
        template = get_template_from_string(u"""
            {% load uni_form_tags %}
            {% uni_form form form_helper %}
        """)
        
        c = Context({'form': TestForm(), 'form_helper': form_helper})        
        html = template.render(c)

        # NOTE: Not sure why this is commented
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
        form_helper = FormHelper()    
        form_helper.form_id = 'this-form-rocks'
        form_helper.form_class = 'forms-that-rock'
        form_helper.form_method = 'GET'
    
        template = get_template_from_string(u"""
            {% load uni_form_tags %}
            {% uni_form form form_helper %}
        """)        

        # now we render it
        c = Context({'form': TestForm(), 'form_helper': form_helper})            
        html = template.render(c)        
        
        # Lets make sure everything loads right
        self.assertTrue('<form' in html)                
        self.assertTrue('class="uniForm forms-that-rock"' in html)
        self.assertTrue('method="get"' in html)
        self.assertTrue('id="this-form-rocks">' in html)        
        
        # now lets remove the form tag and render it again. All the True items above
        # should now be false because the form tag is removed.
        form_helper.form_tag = False
        html = template.render(c)        

        self.assertFalse('<form' in html)        
        self.assertFalse('class="uniForm forms-that-rock"' in html)
        self.assertFalse('method="get"' in html)
        self.assertFalse('id="this-form-rocks">' in html)

    def test_csrf_token_POST_form(self):
        # TODO: remove when pre-CSRF token templatetags are no longer supported
        is_old_django = getattr(settings, 'OLD_DJANGO', False) 
        if not is_old_django:
            form_helper = FormHelper()    
            template = get_template_from_string(u"""
                {% load uni_form_tags %}
                {% uni_form form form_helper %}
            """)        

            # The middleware only initializes the CSRF token when processing a real request
            # So using RequestContext or csrf(request) here does not work.
            # Instead I set the key `csrf_token` to a CSRF manually, which csrf_token tag
            # reads to put a hidden input in > django.template.defaulttags.CsrfTokenNode
            # This way we don't need to use Django's client, have a test_app and urls
            # I like self-contained tests :) CSRF could be any number, we don't care
            c = Context({'form': TestForm(), 'form_helper': form_helper, 'csrf_token': _get_new_csrf_key()})
            html = template.render(c)

            self.assertTrue("<input type='hidden' name='csrfmiddlewaretoken'" in html)                

    def test_csrf_token_GET_form(self):
        form_helper = FormHelper()    
        form_helper.form_method = 'GET'
        template = get_template_from_string(u"""
            {% load uni_form_tags %}
            {% uni_form form form_helper %}
        """)        

        c = Context({'form': TestForm(), 'form_helper': form_helper, 'csrf_token': _get_new_csrf_key()})
        html = template.render(c)
        
        self.assertFalse("<input type='hidden' name='csrfmiddlewaretoken'" in html)                
