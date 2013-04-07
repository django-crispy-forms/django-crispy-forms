from __future__ import with_statement
import inspect
import logging
import sys

from django.conf import settings
from django.forms.forms import BoundField
from django.template import Context
from django.template.loader import get_template
from django.utils.html import conditional_escape
from django.utils.functional import memoize

from base import KeepContext

# Global field template, default template used for rendering a field.

TEMPLATE_PACK = getattr(settings, 'CRISPY_TEMPLATE_PACK', 'bootstrap')

# By memoizeing we avoid loading the template every time render_field
# is called without a template
def default_field_template(template_pack=TEMPLATE_PACK):
    return get_template("%s/field.html" % template_pack)
default_field_template = memoize(default_field_template, {}, 1)


def render(field_name, field_instance, form, form_style, context, template=None, labelclass=None, layout_object=None, attrs=None, template_pack=TEMPLATE_PACK):
    """
    Renders a Django field a la crispy-forms way.
    """
    FAIL_SILENTLY = getattr(settings, 'CRISPY_FAIL_SILENTLY', True)

    # Injecting HTML attributes into field's widget, Django handles rendering these
    try:
        if attrs is not None:
            widgets = getattr(field_instance.widget, 'widgets', [field_instance.widget,])

            # We use attrs as a dictionary later, so here we make a copy
            list_attrs = attrs
            if isinstance(attrs, dict):
                list_attrs = [attrs] * len(widgets)

            for index, (widget, attr) in enumerate(zip(widgets, list_attrs)):
                if hasattr(field_instance.widget, 'widgets'):
                    if 'type' in attr and attr['type'] == "hidden":
                        field_instance.widget.widgets[index].is_hidden = True
                        field_instance.widget.widgets[index] = field_instance.hidden_widget()

                    field_instance.widget.widgets[index].attrs.update(attr)
                else:
                    if 'type' in attr and attr['type'] == "hidden":
                        field_instance.widget.is_hidden = True
                        field_instance.widget = field_instance.hidden_widget()

                    field_instance.widget.attrs.update(attr)
    except KeyError:
        if not FAIL_SILENTLY:
            raise Exception("Could not resolve form field '%s'." % field)
        else:
            field_instance = None
            logging.warning("Could not resolve form field '%s'." % field, exc_info=sys.exc_info())

    if not hasattr(form, 'rendered_fields'):
        form.rendered_fields = set()

    if not field_name in form.rendered_fields:
        form.rendered_fields.add(field_name)
    else:
        if not FAIL_SILENTLY:
            raise Exception("A field should only be rendered once: %s" % field_name)
        else:
            logging.warning("A field should only be rendered once: %s" % field_name, exc_info=sys.exc_info())

    if field_instance is None:
        html = ''
    else:
        bound_field = BoundField(form, field_instance, field_name)

        if template is None:
            template = default_field_template(template_pack)
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
        html = template.render(context)

    return html


def render_layout_object(field, form_or_renderer, form_style, context, template_pack=TEMPLATE_PACK):
    """
    Check if field is a layout object, if so call its render method and return result,
    otherwise return None
    """
    if hasattr(field, 'render'):
        if 'template_pack' in inspect.getargspec(field.render)[0]:
            return field.render(form_or_renderer, form_style, context, template_pack=template_pack)
        else:
            return field.render(form_or_renderer, form_style, context)


def field_to_str(field):
    """
    Convert field to str
    """
    try:
        # This allows fields to be unicode strings, always they don't use non ASCII
        if isinstance(field, unicode):
            return str(field)
        else:
            # If `field` is not unicode then we turn it into a unicode string, otherwise doing
            # str(field) would give no error and the field would not be resolved, causing confusion
            return str(unicode(field))
    except (UnicodeEncodeError, UnicodeDecodeError):
        raise Exception("Field '%s' is using forbidden unicode characters" % field)


def render_field(field, form, form_style, context, template=None, labelclass=None, layout_object=None, attrs=None, template_pack=TEMPLATE_PACK):
    """
    Renders a `field` of a `FormHelper` layout

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
    """
    with KeepContext(context):
        FAIL_SILENTLY = getattr(settings, 'CRISPY_FAIL_SILENTLY', True)

        html = render_layout_object(field, form, form_style, context, template_pack=template_pack)
        if html is not None:
            return html
        field = field_to_str(field)

        try:
            field_instance = form.fields[field]
        except KeyError:
            if not FAIL_SILENTLY:
                raise Exception("Could not resolve form field '%s'." % field)
            else:
                field_instance = None
                logging.warning("Could not resolve form field '%s'." % field, exc_info=sys.exc_info())

        return render(field, field_instance, form, form_style, context,
            template=template, labelclass=labelclass, layout_object=layout_object,
            attrs=attrs, template_pack=template_pack)


def render_field_multiple(field, renderer, form_style, context, template=None, labelclass=None, layout_object=None, attrs=None, template_pack=TEMPLATE_PACK):
    """
    Renders a `field` of a MultipleFormRenderer layout, this field can be a layout object or a string
    """
    with KeepContext(context):
        FAIL_SILENTLY = getattr(settings, 'CRISPY_FAIL_SILENTLY', True)

        html = render_layout_object(field, renderer, form_style, context, template_pack=template_pack)
        if html is not None:
            return html
        field = field_to_str(field)

        # Get form_name and field_name "form_name.field_name"
        try:
            form_name, field_name = field.split(".")
        except ValueError:
            # Here we need to render the whole form
            form_name = field
            return render_crispy_form(renderer.form_mapping[form_name], context=context)

        # Get the form instance
        try:
            form = renderer.form_mapping[form_name]
        except KeyError:
            if not FAIL_SILENTLY:
                raise Exception("Could not resolve form name." % form_name)
            else:
                field_instance = None
                logging.warning("Could not resolve form field '%s'." % form_name, exc_info=sys.exc_info())

        # Get the field instance
        try:
            field_instance = form.fields[field_name]
        except KeyError:
            if not FAIL_SILENTLY:
                raise Exception("Could not resolve form field '%s'." % field_name)
            else:
                field_instance = None
                logging.warning("Could not resolve form field '%s'." % field, exc_info=sys.exc_info())

        return render(field_name, field_instance, form, form_style, context,
            template=template, labelclass=labelclass, layout_object=layout_object,
            attrs=attrs, template_pack=template_pack)


def flatatt(attrs):
    """
    Taken from django.core.utils
    Convert a dictionary of attributes to a single string.
    The returned string will contain a leading space followed by key="value",
    XML-style pairs.  It is assumed that the keys do not need to be XML-escaped.
    If the passed dictionary is empty, then return an empty string.
    """
    return u''.join([u' %s="%s"' % (k.replace('_', '-'), conditional_escape(v)) for k, v in attrs.items()])


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
