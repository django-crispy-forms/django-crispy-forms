from django.template import Context, Template
from django.template.loader import get_template
from django import template


register = template.Library()

@register.filter
def as_uni_form(form):
    template = get_template('uni_form/uni_form.html')
    c = Context({'form':form})

    return template.render(c)
    
