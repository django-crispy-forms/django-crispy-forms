import logging
import sys
from functools import lru_cache

from django.conf import settings
from django.forms.utils import flatatt as _flatatt
from django.template import Context
from django.template.loader import get_template
from django.utils.functional import SimpleLazyObject
from django.utils.safestring import SafeString

from .base import KeepContext


def get_template_pack():
    return getattr(settings, "CRISPY_TEMPLATE_PACK")


TEMPLATE_PACK = SimpleLazyObject(get_template_pack)


# By caching we avoid loading the template every time render_field
# is called without a template
@lru_cache()
def default_field_template(template_pack=TEMPLATE_PACK):
    return get_template("%s/field.html" % template_pack)


def render_field(
    field,
    form,
    context,
    template=None,
    labelclass=None,
    layout_object=None,
    attrs=None,
    template_pack=TEMPLATE_PACK,
    extra_context=None,
    **kwargs,
):
    """
    Renders a django-crispy-forms field

    :param field: Can be a string or a Layout object like `Row`. If it's a layout
        object, we call its render method, otherwise we instantiate a BoundField
        and render it using default template 'CRISPY_TEMPLATE_PACK/field.html'
        The field is added to a list that the form holds called `rendered_fields`
        to avoid double rendering fields.
    :param form: The form/formset to which that field belongs to.
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
            return SafeString("")

        FAIL_SILENTLY = getattr(settings, "CRISPY_FAIL_SILENTLY", True)

        if hasattr(field, "render"):
            return field.render(form, context, template_pack=template_pack)

        try:
            # Injecting HTML attributes into field's widget, Django handles rendering these
            bound_field = form[field]
            field_instance = bound_field.field
            if attrs is not None:
                widgets = getattr(field_instance.widget, "widgets", [field_instance.widget])

                # We use attrs as a dictionary later, so here we make a copy
                list_attrs = attrs
                if isinstance(attrs, dict):
                    list_attrs = [attrs] * len(widgets)

                for index, (widget, attr) in enumerate(zip(widgets, list_attrs)):
                    if hasattr(field_instance.widget, "widgets"):
                        if "type" in attr and attr["type"] == "hidden":
                            field_instance.widget.widgets[index] = field_instance.hidden_widget(attr)

                        else:
                            field_instance.widget.widgets[index].attrs.update(attr)
                    else:
                        if "type" in attr and attr["type"] == "hidden":
                            field_instance.widget = field_instance.hidden_widget(attr)

                        else:
                            field_instance.widget.attrs.update(attr)

        except KeyError:
            if not FAIL_SILENTLY:
                raise Exception("Could not resolve form field '%s'." % field)
            else:
                field_instance = None
                logging.warning("Could not resolve form field '%s'." % field, exc_info=sys.exc_info())

        if hasattr(form, "rendered_fields"):
            if field not in form.rendered_fields:
                form.rendered_fields.add(field)
            else:
                if not FAIL_SILENTLY:
                    raise Exception("A field should only be rendered once: %s" % field)
                else:
                    logging.warning("A field should only be rendered once: %s" % field, exc_info=sys.exc_info())

        if field_instance is None:
            html = SafeString("")
        else:
            if template is None:
                if form.crispy_field_template is None:
                    template = default_field_template(template_pack)
                else:  # FormHelper.field_template set
                    template = get_template(form.crispy_field_template)
            else:
                template = get_template(template)

            # We save the Layout object's bound fields in the layout object's `bound_fields` list
            if layout_object is not None:
                if hasattr(layout_object, "bound_fields") and isinstance(layout_object.bound_fields, list):
                    layout_object.bound_fields.append(bound_field)
                else:
                    layout_object.bound_fields = [bound_field]

            context.update(
                {
                    "field": bound_field,
                    "labelclass": labelclass,
                    "flat_attrs": flatatt(attrs if isinstance(attrs, dict) else {}),
                }
            )
            if extra_context is not None:
                context.update(extra_context)

            html = template.render(context.flatten())

        return html


def flatatt(attrs):
    """
    Convert a dictionary of attributes to a single string.

    Passed attributes are redirected to `django.forms.utils.flatatt()`
    with replaced "_" (underscores) by "-" (dashes) in their names.
    """
    return _flatatt({k.replace("_", "-"): v for k, v in attrs.items()})


def render_crispy_form(form, helper=None, context=None):
    """
    Renders a form and returns its HTML output.

    This function wraps the template logic in a function easy to use in a Django view.
    """
    from crispy_forms.templatetags.crispy_forms_tags import CrispyFormNode

    if helper is not None:
        node = CrispyFormNode("form", "helper")
    else:
        node = CrispyFormNode("form", None)

    node_context = Context(context)
    node_context.update({"form": form, "helper": helper})

    return node.render(node_context)


def list_intersection(list1, list2):
    """
    Take the not-in-place intersection of two lists, similar to sets but preserving order.
    Does not check unicity of list1.
    """
    return [item for item in list1 if item in list2]


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
