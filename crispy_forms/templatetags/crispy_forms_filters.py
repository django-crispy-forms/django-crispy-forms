# -*- coding: utf-8 -*-
from django.conf import settings
from django.forms.formsets import BaseFormSet
from django.template import Context
from django.template.loader import get_template
from django.utils.functional import memoize
from django import template


TEMPLATE_PACK = getattr(settings, 'CRISPY_TEMPLATE_PACK', 'bootstrap')
def uni_formset_template(template_pack=TEMPLATE_PACK):
    return get_template('%s/uni_formset.html' % template_pack)
uni_formset_template = memoize(uni_formset_template, {}, 1)


def uni_form_template(template_pack=TEMPLATE_PACK):
    return get_template('%s/uni_form.html' % template_pack)
uni_form_template = memoize(uni_form_template, {}, 1)

register = template.Library()

@register.filter(name='as_uni_form')
@register.filter(name='crispy')
def as_crispy_form(form, template_pack=TEMPLATE_PACK):
    """
    The original and still very useful way to generate a div elegant form/formset::

        {% load crispy_forms_tags %}

        <form class="uniForm" method="post">
            {% csrf_token %}
            {{ myform|crispy }}
        </form>

        or, if you want to explicitly set the template pack
        {{ myform|crispy:"bootstrap" }}
    """
    if isinstance(form, BaseFormSet):
        template = uni_formset_template(template_pack)
        c = Context({'formset': form, 'form_show_errors': True})
    else:
        template = uni_form_template(template_pack)
        c = Context({'form': form, 'form_show_errors': True})
    return template.render(c)

@register.filter(name='as_uni_errors')
@register.filter(name='as_crispy_errors')
def as_crispy_errors(form, template_pack=TEMPLATE_PACK):
    """
    Renders only form errors the same way as django-crispy-forms::

        {% load crispy_forms_tags %}
        {{ form|as_crispy_errors }}
        or
        {{ form|as_crispy_errors:"bootstrap" }}
    """
    if isinstance(form, BaseFormSet):
        template = get_template('%s/errors_formset.html' % template_pack)
        c = Context({'formset': form})
    else:
        template = get_template('%s/errors.html' % template_pack)
        c = Context({'form':form})
    return template.render(c)


@register.filter(name='as_uni_field')
@register.filter(name='as_crispy_field')
def as_crispy_field(field, template_pack=TEMPLATE_PACK):
    """
    Renders a form field like a django-crispy-forms field::

        {% load crispy_forms_tags %}
        {{ form.field|as_crispy_field }}
        or
        {{ form.field|as_crispy_field:"bootstrap" }}
    """
    template = get_template('%s/field.html' % template_pack)
    c = Context({'field':field, 'form_show_errors': True})
    return template.render(c)
