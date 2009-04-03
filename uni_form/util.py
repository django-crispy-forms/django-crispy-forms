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


class FormHelper(object):
    """
        By setting attributes to me you can easily create the text that goes 
        into the uni_form template tag.
        
        >>> from uni_form.util import FormHelper
        >>> helper = FormHelper()
        >>> helper.form_id = 'my-uni-form-id'
        >>> helper.form_class = 'form1'
        >>> submit = Submit('submit-name','Submit me!')
        >>> helper.add_input(submit)
        >>> button = Button('button-thingee','a button')                
        >>> helper.add_input(button)        
        >>> response_dict ={'helper':helper()}
        >>> render_to_response('my-template.html',response_dict)
        
        {% with form.form_help as form_help %}
            {{ form_help }}
            {% uni_form form form_help %}

        {% endwith %}        
    """
    
    def __init__(self):
        
        self.form_id = ''
        self.form_class = ''
        self.inputs = []
        
    def add_input(self,input_object):
        
        self.inputs.append(input_object)        
        
    def __call__(self):
        items = []
        if self.form_id:
            items.append('id='+self.form_id.strip())
            
        if self.form_class:
            items.append('class='+self.form_class.strip())
            
        if self.inputs:
            print 'blah'
            for inp in self.inputs:
                items.append(inp())
                
        return ';'.join(items)
        
        
        
