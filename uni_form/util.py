"""
class: add space seperated classes to the class list. Always starts with uniform::

    class=<my-first-custom-form-class> <my-custom-form-class>

button: for adding of generic buttons. The name also becomes the slugified id::

    button=<my-custom-button-name>|<my-custom-button-value>

submit: For adding of submt buttons. The name also becomes the slugified id::

    submit=<my-custom-submit-name>|<my-custom-submit-value>

hidden: For adding of hidden buttons::

    hidden=<my-custom-hidden-name>|<my-custom-hidden-value>
"""


class BaseInput(object):

    def __init__(self,name,value):
        self.name = name
        self.value = value

        
    def __call__(self):

        return '%s=%s|%s' % (self.input_type, self.name, self.value)
    
class Submit(BaseInput):

    input_type = 'submit'    


class Button(BaseInput):

    input_type = 'button'    


class Hidden(BaseInput):

    input_type = 'hidden'    


class UniForm(object):
    """
        By setting attributes to me you can easily create the text that goes 
        into the uni_form template tag.
        
        >>> from uni_form.util import UniForm
        >>> uniform = UniForm()
        >>> uniform.form_id = 'my-uni-form-id'
        >>> uniform.form_class = 'form1'
        >>> submit = Submit('submit-name','Submit me!')
        >>> uniform.set_input(submit)
        >>> button = Button('button-thingee','a button')                
        >>> uniform.set_input(button)        
        >>> response_dict ={'form_attrs':uniform()}
        >>> render_to_response()
    """
    
    def __init__(self):
        
        self.form_id = ''
        self.form_class = ''
        self.inputs = []
        
    def set_input(self,input_object):
        
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
                
        return ';'.join(items)
        
        
        
