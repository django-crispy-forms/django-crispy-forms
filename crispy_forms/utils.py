from __future__ import unicode_literals
import logging
import sys

import django
from django.conf import settings
from django.forms.forms import BoundField
from django.template import Context
from django.template.loader import get_template
from django.utils.html import conditional_escape

from .base import KeepContext
from .compatibility import lru_cache, text_type, PY2, SimpleLazyObject


def get_template_pack():
    return getattr(settings, 'CRISPY_TEMPLATE_PACK', 'bootstrap')


TEMPLATE_PACK = SimpleLazyObject(get_template_pack)


# By caching we avoid loading the template every time render_field
# is called without a template
@lru_cache()
def default_field_template(template_pack=TEMPLATE_PACK):
    return get_template("%s/field.html" % template_pack)


def set_hidden(widget):
    """
    set widget to hidden

    different starting in Django 1.7, when is_hidden ceases to be a
    true attribute and is determined by the input_type attribute
    """
    widget.input_type = 'hidden'
    if not widget.is_hidden:
        widget.is_hidden = True


def render_field(
    field, form, form_style, context, template=None, labelclass=None,
    layout_object=None, attrs=None, template_pack=TEMPLATE_PACK,
    extra_context=None, **kwargs
):
    """
    Renders a django-crispy-forms field

    :param field: Can be a string or a Layout object like `Row`. If it's a layout
        object, we call its render method, otherwise we instantiate a BoundField
        and render it using default template 'CRISPY_TEMPLATE_PACK/field.html'
        The field is added to a list that the form holds called `rendered_fields`
        to avoid double rendering fields.
    :param form: The form/formset to which that field belongs to.
    :param form_style: A way to pass style name to the CSS framework used.
    :template: Template used for rendering the field.
    :layout_object: If passed, it points to the Layout object that is being rendered.
        We use it to store its bound fields in a list called `layout_object.bound_fields`
    :attrs: Attributes for the field's widget
    :template_pack: Name of the template pack to be used for rendering `field`
    :extra_context: Dictionary to be added to context, added variables by the layout object
    """
    added_keys = [] if extra_context is None else extra_context.keys()
    with KeepContext(context, added_keys):
        if field is None:
            return ''

        FAIL_SILENTLY = getattr(settings, 'CRISPY_FAIL_SILENTLY', True)

        if hasattr(field, 'render'):
            return field.render(
                form, form_style, context, template_pack=template_pack,
            )
        else:
            # In Python 2 form field names cannot contain unicode characters without ASCII mapping
            if PY2:
                # This allows fields to be unicode strings, always they don't use non ASCII
                try:
                    if isinstance(field, text_type):
                        field = field.encode('ascii').decode()
                    # If `field` is not unicode then we turn it into a unicode string, otherwise doing
                    # str(field) would give no error and the field would not be resolved, causing confusion
                    else:
                        field = text_type(field)

                except (UnicodeEncodeError, UnicodeDecodeError):
                    raise Exception("Field '%s' is using forbidden unicode characters" % field)

        try:
            # Injecting HTML attributes into field's widget, Django handles rendering these
            field_instance = form.fields[field]
            if attrs is not None:
                widgets = getattr(field_instance.widget, 'widgets', [field_instance.widget])

                # We use attrs as a dictionary later, so here we make a copy
                list_attrs = attrs
                if isinstance(attrs, dict):
                    list_attrs = [attrs] * len(widgets)

                for index, (widget, attr) in enumerate(zip(widgets, list_attrs)):
                    if hasattr(field_instance.widget, 'widgets'):
                        if 'type' in attr and attr['type'] == "hidden":
                            set_hidden(field_instance.widget.widgets[index])
                            field_instance.widget.widgets[index] = field_instance.hidden_widget()

                        field_instance.widget.widgets[index].attrs.update(attr)
                    else:
                        if 'type' in attr and attr['type'] == "hidden":
                            set_hidden(field_instance.widget)
                            field_instance.widget = field_instance.hidden_widget()

                        field_instance.widget.attrs.update(attr)

        except KeyError:
            if not FAIL_SILENTLY:
                raise Exception("Could not resolve form field '%s'." % field)
            else:
                field_instance = None
                logging.warning("Could not resolve form field '%s'." % field, exc_info=sys.exc_info())

        if hasattr(form, 'rendered_fields'):
            if not field in form.rendered_fields:
                form.rendered_fields.add(field)
            else:
                if not FAIL_SILENTLY:
                    raise Exception("A field should only be rendered once: %s" % field)
                else:
                    logging.warning("A field should only be rendered once: %s" % field, exc_info=sys.exc_info())

        if field_instance is None:
            html = ''
        else:
            bound_field = BoundField(form, field_instance, field)

            if template is None:
                if form.crispy_field_template is None:
                    template = default_field_template(template_pack)
                else:   # FormHelper.field_template set
                    template = get_template(form.crispy_field_template)
            else:
                template = get_template(template)

            # We save the Layout object's bound fields in the layout object's `bound_fields` list
            if layout_object is not None:
                if hasattr(layout_object, 'bound_fields') and isinstance(layout_object.bound_fields, list):
                    layout_object.bound_fields.append(bound_field)
                else:
                    layout_object.bound_fields = [bound_field]

            context.update({
                'field': bound_field,
                'labelclass': labelclass,
                'flat_attrs': flatatt(attrs if isinstance(attrs, dict) else {}),
            })
            if extra_context is not None:
                context.update(extra_context)

            if django.VERSION >= (1, 8):
                context = context.flatten()

            html = template.render(context)

        return html


def flatatt(attrs):
    """
    Taken from django.core.utils
    Convert a dictionary of attributes to a single string.
    The returned string will contain a leading space followed by key="value",
    XML-style pairs.  It is assumed that the keys do not need to be XML-escaped.
    If the passed dictionary is empty, then return an empty string.
    """
    return ''.join([' %s="%s"' % (k.replace('_', '-'), conditional_escape(v)) for k, v in attrs.items()])


def render_crispy_form(form, helper=None, context=None):
    """
    Renders a form and returns its HTML output.

    This function wraps the template logic in a function easy to use in a Django view.
    """
    from crispy_forms.templatetags.crispy_forms_tags import CrispyFormNode

    if helper is not None:
        node = CrispyFormNode('form', 'helper')
    else:
        node = CrispyFormNode('form', None)

    node_context = Context(context)
    node_context.update({
        'form': form,
        'helper': helper
    })

    return node.render(node_context)


def list_intersection(list1, list2):
    """
    Take the not-in-place intersection of two lists, similar to sets but preserving order.
    Does not check unicity of list1.
    """
    intersection = []
    for item in list1:
        if item in list2:
            intersection.append(item)
    return intersection


def list_union(*lists):
    """
    Take the not-in-place union of two or more lists, similar to sets but preserving order.
    """
    union = []
    for li in lists:
        for item in li:
            if item not in union:
                union.append(item)
    return union


def list_difference(left, right):
    """
    Take the not-in-place difference of two lists (left - right), similar to sets but preserving order.
    """
    blocked = set(right)
    difference = []
    for item in left:
        if item not in blocked:
            blocked.add(item)
            difference.append(item)
    return difference


