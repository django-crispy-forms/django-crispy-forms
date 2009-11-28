from django import template

register = template.Library()

class_converter = {
    "textinput":"textinput textInput",
    "fileinput":"fileinput fileUpload"
}

@register.filter
def is_checkbox(field):
    return field.field.widget.__class__.__name__.lower() == "checkboxinput"

@register.filter
def with_class(field):
    class_name = field.field.widget.__class__.__name__.lower()
    class_name = class_converter.get(class_name, class_name)
    if "class" in field.field.widget.attrs:
        field.field.widget.attrs['class'] += " %s" % class_name
    else:
        field.field.widget.attrs['class'] = class_name
    return unicode(field)


