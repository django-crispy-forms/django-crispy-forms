from django import template

register = template.Library()

class_converter = {
    "textinput":"textinput textInput",
    "fileinput":"fileinput fileUpload",
    "passwordinput":"passwordinput textInput"
}

@register.filter
def is_checkbox(field):
    return field.field.widget.__class__.__name__.lower() == "checkboxinput"

@register.filter
def with_class(field):
    class_name = field.field.widget.__class__.__name__.lower()
    class_name = class_converter.get(class_name, class_name)
    if "class" in field.field.widget.attrs:
        css_class = field.field.widget.attrs['class']
        if field.field.widget.attrs['class'].find(class_name) == -1:
            css_class += " %s" % (class_name,)
    else:
        css_class = class_name

    return field.as_widget(attrs={'class': css_class})    





