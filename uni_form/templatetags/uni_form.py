from django.template import Context, Template
from django.template.loader import get_template
from django import template


register = template.Library()

@register.filter
def as_uni_form(form):
    template = get_template('uni_form/uni_form.html')
    c = Context({'form':form})
    return template.render(c)
    
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
    
