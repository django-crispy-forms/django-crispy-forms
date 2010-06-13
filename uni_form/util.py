from django import forms
from django.forms.widgets import Input

class SubmitButtonWidget(Input):
    """
    A widget that handles a submit button.
    """
    input_type = 'submit'

    def render(self, name, value, attrs=None):
        return super(SubmitButtonWidget, self).render(name,
            self.attrs['value'], attrs)
        
        
class BaseInput(forms.Field):
    """
        An base Input class to reduce the amount of code in the Input classes.
    """
    widget = SubmitButtonWidget

    def __init__(self, **kwargs):
        if not 'label' in kwargs:
            kwargs['label'] = ''
        if not 'required' in kwargs:
            kwargs['required'] = False
        if 'value' in kwargs:
            self._widget_attrs = {'value': kwargs['value']}
            del kwargs['value']
        else:
            self._widget_attrs = {'value': 'Submit'}
        super(BaseInput, self).__init__(**kwargs)

    def widget_attrs(self, widget):
        return self._widget_attrs

class Toggle(object):
    """
        A container for holder toggled items such as fields and buttons.
    """
    
    fields = []