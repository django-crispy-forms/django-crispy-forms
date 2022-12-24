from functools import lru_cache

from django import template
from django.conf import settings
from django.forms import boundfield
from django.forms.formsets import BaseFormSet
from django.template.loader import get_template
from django.utils.safestring import mark_safe

from crispy_forms.exceptions import CrispyError
from crispy_forms.utils import TEMPLATE_PACK, flatatt


@lru_cache()
def uni_formset_template(template_pack=TEMPLATE_PACK):
    return get_template("%s/uni_formset.html" % template_pack)


@lru_cache()
def uni_form_template(template_pack=TEMPLATE_PACK):
    return get_template("%s/uni_form.html" % template_pack)


register = template.Library()


@register.filter(name="crispy")
def as_crispy_form(form, template_pack=TEMPLATE_PACK, label_class="", field_class=""):
    """
    The original and still very useful way to generate a div elegant form/formset::

        {% load crispy_forms_tags %}

        <form class="my-class" method="post">
            {% csrf_token %}
            {{ myform|crispy }}
        </form>

    or, if you want to explicitly set the template pack::

        {{ myform|crispy:"bootstrap4" }}

    In ``bootstrap3`` or ``bootstrap4`` for horizontal forms you can do::

        {{ myform|label_class:"col-lg-2",field_class:"col-lg-8" }}
    """
    c = {
        "field_class": field_class,
        "field_template": "%s/field.html" % template_pack,
        "form_show_errors": True,
        "form_show_labels": True,
        "label_class": label_class,
    }
    if isinstance(form, BaseFormSet):
        template = uni_formset_template(template_pack)
        c["formset"] = form
    else:
        template = uni_form_template(template_pack)
        c["form"] = form

    return template.render(c)


@register.filter(name="as_crispy_errors")
def as_crispy_errors(form, template_pack=TEMPLATE_PACK):
    """
    Renders only form errors the same way as django-crispy-forms::

        {% load crispy_forms_tags %}
        {{ form|as_crispy_errors }}

    or::

        {{ form|as_crispy_errors:"bootstrap4" }}
    """
    if isinstance(form, BaseFormSet):
        template = get_template("%s/errors_formset.html" % template_pack)
        c = {"formset": form}
    else:
        template = get_template("%s/errors.html" % template_pack)
        c = {"form": form}

    return template.render(c)


@register.filter(name="as_crispy_field")
def as_crispy_field(field, template_pack=TEMPLATE_PACK, label_class="", field_class=""):
    """
    Renders a form field like a django-crispy-forms field::

        {% load crispy_forms_tags %}
        {{ form.field|as_crispy_field }}

    or::

        {{ form.field|as_crispy_field:"bootstrap4" }}
    """
    if not isinstance(field, boundfield.BoundField) and settings.DEBUG:
        raise CrispyError("|as_crispy_field got passed an invalid or inexistent field")

    attributes = {
        "field": field,
        "form_show_errors": True,
        "form_show_labels": True,
        "label_class": label_class,
        "field_class": field_class,
    }
    helper = getattr(field.form, "helper", None)

    template_path = None
    if helper is not None:
        attributes.update(helper.get_attributes(template_pack))
        template_path = helper.field_template
    if not template_path:
        template_path = "%s/field.html" % template_pack
    template = get_template(template_path)

    return template.render(attributes)


@register.filter(name="flatatt")
def flatatt_filter(attrs):
    return mark_safe(flatatt(attrs))


@register.filter
def optgroups(field):
    """
    A template filter to help rendering of fields with optgroups.

    Returns:
        A tuple of label, option, index

        label: Group label for grouped optgroups (`None` if inputs are not
               grouped).

        option: A dict containing information to render the option::

            {
                "name": "checkbox_select_multiple",
                "value": 1,
                "label": 1,
                "selected": False,
                "index": "0",
                "attrs": {"id": "id_checkbox_select_multiple_0"},
                "type": "checkbox",
                "template_name": "django/forms/widgets/checkbox_option.html",
                "wrap_label": True,
            }

        index: Group index

    """
    id_ = field.field.widget.attrs.get("id") or field.auto_id
    attrs = {"id": id_} if id_ else {}
    attrs = field.build_widget_attrs(attrs)
    values = field.field.widget.format_value(field.value())
    return field.field.widget.optgroups(field.html_name, values, attrs)
