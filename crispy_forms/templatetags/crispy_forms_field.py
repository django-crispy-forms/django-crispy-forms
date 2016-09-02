try:
    from itertools import izip
except ImportError:
    izip = zip

import django
from django import forms
from django import template
from django.template import loader, Context
from django.conf import settings

from crispy_forms.utils import TEMPLATE_PACK, get_template_pack

register = template.Library()


@register.filter
def is_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxInput)


@register.filter
def is_password(field):
    return isinstance(field.field.widget, forms.PasswordInput)


@register.filter
def is_radioselect(field):
    return isinstance(field.field.widget, forms.RadioSelect)


@register.filter
def is_select(field):
    return isinstance(field.field.widget, forms.Select)


@register.filter
def is_checkboxselectmultiple(field):
    return isinstance(field.field.widget, forms.CheckboxSelectMultiple)


@register.filter
def is_file(field):
    return isinstance(field.field.widget, forms.ClearableFileInput)


@register.filter
def classes(field):
    """
    Returns CSS classes of a field
    """
    return field.widget.attrs.get('class', None)


@register.filter
def css_class(field):
    """
    Returns widgets class name in lowercase
    """
    return field.field.widget.__class__.__name__.lower()


def pairwise(iterable):
    """s -> (s0,s1), (s2,s3), (s4, s5), ..."""
    a = iter(iterable)
    return izip(a, a)


class CrispyFieldNode(template.Node):
    def __init__(self, field, attrs):
        self.field = field
        self.attrs = attrs
        self.html5_required = 'html5_required'

    def render(self, context):
        # Nodes are not threadsafe so we must store and look up our instance
        # variables in the current rendering context first
        if self not in context.render_context:
            context.render_context[self] = (
                template.Variable(self.field),
                self.attrs,
                template.Variable(self.html5_required)
            )

        field, attrs, html5_required = context.render_context[self]
        field = field.resolve(context)
        try:
            html5_required = html5_required.resolve(context)
        except template.VariableDoesNotExist:
            html5_required = False

        # If template pack has been overridden in FormHelper we can pick it from context
        template_pack = context.get('template_pack', TEMPLATE_PACK)

        widgets = getattr(field.field.widget, 'widgets', [field.field.widget])

        if isinstance(attrs, dict):
            attrs = [attrs] * len(widgets)

        converters = {
            'textinput': 'textinput textInput',
            'fileinput': 'fileinput fileUpload',
            'passwordinput': 'textinput textInput',
        }
        converters.update(getattr(settings, 'CRISPY_CLASS_CONVERTERS', {}))

        for widget, attr in zip(widgets, attrs):
            class_name = widget.__class__.__name__.lower()
            class_name = converters.get(class_name, class_name)
            css_class = widget.attrs.get('class', '')
            if css_class:
                if css_class.find(class_name) == -1:
                    css_class += " %s" % class_name
            else:
                css_class = class_name

            if (
                template_pack in ['bootstrap3', 'bootstrap4']
                and not is_checkbox(field)
                and not is_file(field)
            ):
                css_class += ' form-control'
                if field.errors:
                    css_class += ' form-control-danger'

            widget.attrs['class'] = css_class

            # HTML5 required attribute
            if html5_required and field.field.required and 'required' not in widget.attrs:
                if field.field.widget.__class__.__name__ is not 'RadioSelect':
                    widget.attrs['required'] = 'required'

            for attribute_name, attribute in attr.items():
                attribute_name = template.Variable(attribute_name).resolve(context)

                if attribute_name in widget.attrs:
                    widget.attrs[attribute_name] += " " + template.Variable(attribute).resolve(context)
                else:
                    widget.attrs[attribute_name] = template.Variable(attribute).resolve(context)

        return field


@register.tag(name="crispy_field")
def crispy_field(parser, token):
    """
    {% crispy_field field attrs %}
    """
    token = token.split_contents()
    field = token.pop(1)
    attrs = {}

    # We need to pop tag name, or pairwise would fail
    token.pop(0)
    for attribute_name, value in pairwise(token):
        attrs[attribute_name] = value

    return CrispyFieldNode(field, attrs)


@register.simple_tag()
def crispy_addon(field, append="", prepend="", form_show_labels=True):
    """
    Renders a form field using bootstrap's prepended or appended text::

        {% crispy_addon form.my_field prepend="$" append=".00" %}

    You can also just prepend or append like so

        {% crispy_addon form.my_field prepend="$" %}
        {% crispy_addon form.my_field append=".00" %}
    """
    if field:
        context = Context({
            'field': field,
            'form_show_errors': True,
            'form_show_labels': form_show_labels,
        })
        template = loader.get_template('%s/layout/prepended_appended_text.html' % get_template_pack())
        context['crispy_prepended_text'] = prepend
        context['crispy_appended_text'] = append

        if not prepend and not append:
            raise TypeError("Expected a prepend and/or append argument")

        if django.VERSION >= (1, 8):
            context = context.flatten()

    return template.render(context)
