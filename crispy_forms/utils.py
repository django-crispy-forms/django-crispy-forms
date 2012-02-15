import logging
import sys

from django.conf import settings
from django.forms.forms import BoundField
from django.template import Context
from django.template.loader import get_template
from django.forms.util import flatatt


# Global field template, default template used for rendering a field. This way we avoid 
# loading the template every time render_field is called without a template
TEMPLATE_PACK = getattr(settings, 'CRISPY_TEMPLATE_PACK', 'bootstrap')
default_field_template = get_template("%s/field.html" % TEMPLATE_PACK)

def render_field(field, form, form_style, context, template=None, labelclass=None, layout_object=None, attrs=None):
    """
    Renders a django-crispy-forms field
    
    :param field: Can be a string or a Layout object like `Row`. If it's a layout
        object, we call its render method, otherwise we instantiate a BoundField
        and render it using default template 'uni_form/field.html'
        The field is added to a list that the form holds called `rendered_fields`
        to avoid double rendering fields.

    :param form: The form/formset to which that field belongs to.
    
    :param form_style: A way to pass style name to the CSS framework used.

    :template: Template used for rendering the field.

    :layout_object: If passed, it points to the Layout object that is being rendered.
        We use it to store its bound fields in a list called `layout_object.bound_fields`

    :attrs: Attributes for the field's widget
    """
    FAIL_SILENTLY = getattr(settings, 'CRISPY_FAIL_SILENTLY', True)

    if hasattr(field, 'render'):
        return field.render(form, form_style, context)
    else:
        # This allows fields to be unicode strings, always they don't use non ASCII
        try:
            if isinstance(field, unicode):
                field = str(field)
            # If `field` is not unicode then we turn it into a unicode string, otherwise doing
            # str(field) would give no error and the field would not be resolved, causing confusion 
            else:
                field = str(unicode(field))
                
        except (UnicodeEncodeError, UnicodeDecodeError):
            raise Exception("Field '%s' is using forbidden unicode characters" % field)

    try:
        field_instance = form.fields[field]
        if attrs is not None:
            field_instance.widget.attrs.update(attrs)
    except KeyError:
        if not FAIL_SILENTLY:
            raise Exception("Could not resolve form field '%s'." % field)
        else:
            field_instance = None
            logging.warning("Could not resolve form field '%s'." % field, exc_info=sys.exc_info())
            
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
            template = default_field_template
        else:
            template = get_template(template)

        # We save the Layout object's bound fields in the layout object's `bound_fields` list
        if layout_object is not None:
            layout_object.bound_fields.append(bound_field) 
       
        context.update({'field': bound_field, 'labelclass': labelclass, 'flat_attrs': flatatt(attrs or {})})
        html = template.render(context)

    return html
