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
# Everything below is experiamental
####################################
    
    
@register.tag(name="uni_form")    
def do_uni_form(parser, token):
    token = token.split_contents()
    tag_name = token.pop(0)
    try:
        form = token.pop(0)
    except IndexError:
        msg = '%r tag requires a form to process' % token.contents[0] 
        raise template.TemplateSyntaxError(msg) 
        
    if token:
        # we have token elements left, and these must be buttons
        return UniFormNode(form,token)
        
    return UniFormNode(form)
        
class Button(object):
    
    def __init__(self,name,button_type=None,value=None,button_id=None,button_class=None):
        self.name = name
        if button_type:
            self.type = button_type
        else:
            self.type = 'button'
        if value:
            self.value = value
        else:
            self.value = name
        if button_id:
            self.button_id = button_id
        if button_class:
            self.button_class = button_class


class UniFormNode(template.Node):
    def __init__(self,form,buttons=[]):
        self.form = template.Variable(form)
        if buttons:
            self.buttons = buttons
        else:
            self.buttons = ['submit','reset']
            
    def render(self,context):
        template = get_template('uni_form/whole_uni_form.html')
        actual_form = self.form.resolve(context)
        c = Context({'form':actual_form,'buttons':self.buttons})
        return template.render(c)
    
    def do_buttons(self):
        buttons = []
        for button in self.buttons:
            if button.lower() in ('submit','reset'):
                buttons.append(button)
        return buttons
        