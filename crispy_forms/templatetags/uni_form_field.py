from django import template

register = template.Library()

class_converter = {
    "textinput": "textinput textInput",
    "fileinput": "fileinput fileUpload",
    "passwordinput": "textinput textInput",
}

@register.filter
def is_checkbox(field):
    return field.field.widget.__class__.__name__.lower() == "checkboxinput"

@register.filter
def with_class(field):
    class_name = field.field.widget.__class__.__name__.lower()
    class_name = class_converter.get(class_name, class_name)
    
    css_class = field.field.widget.attrs.get('class', '')
    if css_class:
        if css_class.find(class_name) == -1:
            css_class += " %s" % class_name
    else:
        css_class = class_name

    field.field.widget.attrs['class'] = css_class
    return field
