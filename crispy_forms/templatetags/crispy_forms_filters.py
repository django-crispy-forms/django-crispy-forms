# -*- coding: utf-8 -*-
import django
from django.conf import settings
from django.forms import forms
from django.forms.formsets import BaseFormSet
from django.template import Context
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from django import template

from crispy_forms.compatibility import lru_cache
from crispy_forms.exceptions import CrispyError
from crispy_forms.utils import flatatt, TEMPLATE_PACK


@lru_cache()
def uni_formset_template(template_pack=TEMPLATE_PACK):
    return get_template('%s/uni_formset.html' % template_pack)


@lru_cache()
def uni_form_template(template_pack=TEMPLATE_PACK):
    return get_template('%s/uni_form.html' % template_pack)

register = template.Library()


@register.filter(name='crispy')
def as_crispy_form(form, template_pack=TEMPLATE_PACK, label_class="", field_class=""):
    """
    The original and still very useful way to generate a div elegant form/formset::

        {% load crispy_forms_tags %}

        <form class="uniForm" method="post">
            {% csrf_token %}
            {{ myform|crispy }}
        </form>

    or, if you want to explicitly set the template pack::

        {{ myform|crispy:"bootstrap" }}

    In ``bootstrap3`` or ``bootstrap4`` for horizontal forms you can do::

        {{ myform|label_class:"col-lg-2",field_class:"col-lg-8" }}
    """
    if isinstance(form, BaseFormSet):
        template = uni_formset_template(template_pack)
        c = Context({
            'formset': form,
            'form_show_errors': True,
            'form_show_labels': True,
            'label_class': label_class,
            'field_class': field_class,
        })
    else:
        template = uni_form_template(template_pack)
        c = Context({
            'form': form,
            'form_show_errors': True,
            'form_show_labels': True,
            'label_class': label_class,
            'field_class': field_class,
        })

    if django.VERSION >= (1, 8):
        c = c.flatten()

    return template.render(c)


@register.filter(name='as_crispy_errors')
def as_crispy_errors(form, template_pack=TEMPLATE_PACK):
    """
    Renders only form errors the same way as django-crispy-forms::

        {% load crispy_forms_tags %}
        {{ form|as_crispy_errors }}

    or::

        {{ form|as_crispy_errors:"bootstrap" }}
    """
    if isinstance(form, BaseFormSet):
        template = get_template('%s/errors_formset.html' % template_pack)
        c = Context({'formset': form})
    else:
        template = get_template('%s/errors.html' % template_pack)
        c = Context({'form': form})

    if django.VERSION >= (1, 8):
        c = c.flatten()

    return template.render(c)


@register.filter(name='as_crispy_field')
def as_crispy_field(field, template_pack=TEMPLATE_PACK):
    """
    Renders a form field like a django-crispy-forms field::

        {% load crispy_forms_tags %}
        {{ form.field|as_crispy_field }}

    or::

        {{ form.field|as_crispy_field:"bootstrap" }}
    """
    if not isinstance(field, forms.BoundField) and settings.DEBUG:
        raise CrispyError('|as_crispy_field got passed an invalid or inexistent field')

    template = get_template('%s/field.html' % template_pack)
    c = Context({'field': field, 'form_show_errors': True, 'form_show_labels': True})

    if django.VERSION >= (1, 8):
        c = c.flatten()

    return template.render(c)


@register.filter(name='flatatt')
def flatatt_filter(attrs):
    return mark_safe(flatatt(attrs))
