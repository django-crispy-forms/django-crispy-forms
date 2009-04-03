from django.template import Context, Template
from django.template.loader import get_template
from django import template

register = template.Library()

@register.filter
def as_uni_form(form):
    template = get_template('uni_form/uni_form.html')
    c = Context({'form':form})
    return template.render(c)
    
####################################
# Everything below is experimental
####################################
"""
token has up to two objects in it:
    
form: The forms object to be rendered by the tag

attrs: A string of semi-colon seperated attributes that can be applied to the 
form in string format. They are used as follows:

id: applied to the form as a whole. Defaults to empty::

    id=<my-form-id>

class: add space seperated classes to the class list. Always starts with uniform::
    
    class=<my-first-custom-form-class> <my-custom-form-class>
    
button: for adding of generic buttons. The name also becomes the slugified id::

    button=<my-custom-button-name>|<my-custom-button-value>
    
submit: For adding of submt buttons. The name also becomes the slugified id::

    submit=<my-custom-submit-name>|<my-custom-submit-value>

hidden: For adding of hidden buttons::

    hidden=<my-custom-hidden-name>|<my-custom-hidden-value>
    
Example::

    {% uni_form my-form id=my-form-id;button=button-one|button-two;submit=submit|go! %}

"""


@register.tag(name="uni_form")  
def do_uni_form(parser, token): 
    
    token = token.split_contents()

    form = token.pop(1)
    try:
        attrs = token.pop(1)
    except IndexError:
        attrs = None
                

    return UniFormNode(form,attrs)    
    
class UniFormNode(template.Node):    

    def __init__(self,form,attrs):
        self.form = template.Variable(form)
        self.attrs = template.Variable(attrs)        
            
    def render(self,context):
        actual_form = self.form.resolve(context)
        attrs = self.attrs.resolve(context).split(';')
        form_class = ''
        form_id = ''        
        inputs = []
        if attrs:
            for element in attrs:
                key, value = element.split('=')
                key = key.strip()
                value = value.strip()
                
                # we hard code these because these should be hard to change.
                if key == 'id':
                    form_id = value
                    
                if key == 'class':
                    form_class = ' '+ value
                    
                if key in ['button','submit','hidden']:
                    # TODO: Raise description error if 2 values not provided
                    name, value = value.split('|')
                    inputs.append({'name':name,'value':value,'type':key})


        response_dict = {
                        'form':actual_form,
                        'attrs':attrs,
                        'form_class' : form_class,
                        'form_id' : form_id,
                        'inputs' : inputs,
                        }
        c = Context(response_dict)
        template = get_template('uni_form/whole_uni_form.html')        
        return template.render(c)    