from itertools import izip

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
def is_password(field):
    return field.field.widget.__class__.__name__.lower() == "passwordinput"

@register.filter
def css_class(field):
    return field.field.widget.__class__.__name__.lower()

def pairwise(iterable):
    "s -> (s0,s1), (s2,s3), (s4, s5), ..."
    a = iter(iterable)
    return izip(a, a)

class CrispyFieldNode(template.Node):
    def __init__(self, field, attrs):
       self.field = template.Variable(field)
       self.attrs = attrs

    def render(self, context):
        field = self.field.resolve(context)

        class_name = field.field.widget.__class__.__name__.lower()
        class_name = class_converter.get(class_name, class_name)
        
        css_class = field.field.widget.attrs.get('class', '')
        if css_class:
            if css_class.find(class_name) == -1:
                css_class += " %s" % class_name
        else:
            css_class = class_name

        field.field.widget.attrs['class'] = css_class

        for attribute_name, attribute in self.attrs.items():
            field.field.widget.attrs[template.Variable(attribute_name).resolve(context)] = template.Variable(attribute).resolve(context)

        return field

@register.tag(name="crispy_field")
def crispy_field(parser, token):
    """
    {% crispy_field field attrs %}
    """
    token = token.split_contents()
    field = token.pop(1)
    attrs = {}

    tag_name = token.pop(0)
    for attribute_name, value in pairwise(token):
        attrs[attribute_name] = value

    return CrispyFieldNode(field, attrs)
