from django import template
register = template.Library()
from django.utils.safestring import mark_safe



@register.filter
def as_uni_form(form):
    # TODO:
    #   1. Use django template to render the text
    #   2. possible escape the text in the rendered fields
    
    text = ''
    for field in form:
        text += """
            <div class="ctrlHolder">
                %s
                %s : %s
            </div>
        """ % (field.errors, field.label_tag(), field)
    return mark_safe(text)
    

