"""
    Utilities for helping developers use python for adding various attributes,
    elements, and UI elements to forms generated via the uni_form template tag.

"""
from uni_form.util import BaseInput, Toggle
    
class Submit(BaseInput):
    """
        Used to create a Submit button descriptor for the uni_form template tag.    
    """

    input_type = 'submit'    


class Button(BaseInput):
    """
        Used to create a Submit input descriptor for the uni_form template tag.    
    """
    
    input_type = 'button'    


class Hidden(BaseInput):
    """
        Used to create a Hidden input descriptor for the uni_form template tag.    
    """

    input_type = 'hidden'  
    
class Reset(BaseInput):
    """
        Used to create a Hidden input descriptor for the uni_form template tag.    
    """

    input_type = 'reset'      


class FormHelper(object):
    """
        By setting attributes to me you can easily create the text that goes 
        into the uni_form template tag. One use case is to add to your form 
        class.
        
        First we create a MyForm class and instantiate it
        
        >>> from django import forms
        >>> from uni_form.helpers import FormHelper, Submit, Reset
        >>> from django.utils.translation import ugettext_lazy as _
        >>> class MyForm(forms.Form):
        ...     title = forms.CharField(label=_("Title"), max_length=30, widget=forms.TextInput())
        ...     # this displays how to attach a formHelper to your forms class.
        ...     helper = FormHelper()
        ...     helper.form_id = 'this-form-rocks'
        ...     helper.form_class = 'search'
        ...     submit = Submit('search','search this site')
        ...     helper.add_input(submit)
        ...     reset = Reset('reset','reset button')                
        ...     helper.add_input(reset)        
        
        Now lets instantiate the form and investigate it.
        
        >>> my_form = MyForm()
        >>> my_form.helper()
        'id=this-form-rocks;class=search;submit=search|search this site;reset=reset|reset button'
        
        The uni_form.util.FormHelper is returns this string when called because
        django templates can call things this way. So if I had a template called
        by a view that called this form we would use this helper thus::
        
            {% load uni_form %}
        
            {% with form.helper as helper %}
                {% uni_form form helper %}
            {% endwith %}
        
    """
    
    def __init__(self):
        
        self.form_id = ''
        self.form_class = ''
        self.inputs = []
        self.toggle = Toggle()
        
    def add_input(self,input_object):
        
        self.inputs.append(input_object)        
        
    def __call__(self):
        items = []
        if self.form_id:
            items.append('id='+self.form_id.strip())
            
        if self.form_class:
            items.append('class='+self.form_class.strip())
            
        if self.inputs:
            for inp in self.inputs:
                items.append(inp())
                
        if self.toggle.fields:
            items.append('toggle_fields=id_' + ',id_'.join(self.toggle.fields))
                
        return ';'.join(items)
        
        
        
