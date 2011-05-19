# -*- coding: utf-8 -*-
from django.conf import settings
from django.forms.formsets import BaseFormSet
from django.template import Context
from django.template.loader import get_template
from django import template

from uni_form.helpers import FormHelper

register = template.Library()


@register.filter
def as_uni_form(form, arg=None):
    if isinstance(form, BaseFormSet):
        template = get_template('uni_form/uni_formset.html')
        c = Context({'formset': form})
    else:
        template = get_template('uni_form/uni_form.html')
        c = Context({'form': form})
    if arg == "fieldset-open":
        c['fieldset_open'] = True
    return template.render(c)

@register.filter
def as_uni_errors(form):
    if isinstance(form, BaseFormSet):
        template = get_template('uni_form/errors_formset.html')
        c = Context({'formset': form})
    else:
        template = get_template('uni_form/errors.html')
        c = Context({'form':form})
    return template.render(c)

@register.filter
def as_uni_field(field):
    template = get_template('uni_form/field.html')
    c = Context({'field':field})
    return template.render(c)

@register.inclusion_tag("uni_form/includes.html", takes_context=True)
def uni_form_setup(context):
    """
    Creates the <style> and <script> tags needed to initialize the uni-form.

    Create a local uni-form/includes.html template if you want to customize how
    these files are loaded.
    """
    if 'STATIC_URL' not in context:
        context['STATIC_URL'] = settings.STATIC_URL
    return (context)
