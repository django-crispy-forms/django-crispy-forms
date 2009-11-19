from django import forms
from django.template import Context, Template
from django.template.loader import get_template_from_string
from django.test import TestCase

class TestForm(forms.Form):

    is_company = forms.CharField(label="company", required=False, widget=forms.CheckboxInput())    
    email = forms.CharField(label="email", max_length=30, required=True, widget=forms.TextInput())        
    password1 = forms.CharField(label="password", max_length=30, required=True, widget=forms.PasswordInput())
    password2 = forms.CharField(label="re-enter password", max_length=30, required=True, widget=forms.PasswordInput())    
    first_name = forms.CharField(label="first name", max_length=30, required=True, widget=forms.TextInput())        
    last_name = forms.CharField(label="last name", max_length=30, required=True, widget=forms.TextInput())            


class TestTemplateTags(TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_as_uni_form(self):
        
        form = TestForm()

        c = Context({'form':form})
        
        template = get_template_from_string("""
            {% load uni_form_tags %}
            
            {{ form|as_uni_form }}
        """)
        html = template.render(c)
        
        self.assertTrue("<td>" not in html)
        self.assertTrue("id_is_company" in html)

        html = template.render(c)
        
    