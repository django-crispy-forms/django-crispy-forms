# -*- coding: utf-8 -*-
from django.conf import settings
from django.forms.formsets import BaseFormSet
from django.template import Context
from django.template.loader import get_template
from django import template

from uni_form.helpers import FormHelper

uni_formset_template = get_template('uni_form/uni_formset.html')
uni_form_template = get_template('uni_form/uni_form.html')

register = template.Library()

@register.filter
def as_uni_form(form):
    """ 
    The original and still very useful way to generate a uni-form form/formset::
    
        {% load uni_form_tags %}

        <form class="uniForm" action="post">
            {% csrf_token %}
            {{ myform|as_uni_form }}
        </form>
    """
    if isinstance(form, BaseFormSet):
        if settings.DEBUG:
            template = get_template('uni_form/uni_formset.html')
        else:
            template = uni_formset_template
        c = Context({'formset': form})
    else:
        if settings.DEBUG:
            template = get_template('uni_form/uni_form.html')
        else:
            template = uni_form_template
        c = Context({'form': form})
    return template.render(c)

@register.filter
def as_uni_errors(form):
    """
    Renders only form errors like django-uni-form::

        {% load uni_form_tags %}
        {{ form|as_uni_errors }}
    """
    if isinstance(form, BaseFormSet):
        template = get_template('uni_form/errors_formset.html')
        c = Context({'formset': form})
    else:
        template = get_template('uni_form/errors.html')
        c = Context({'form':form})
    return template.render(c)

@register.filter
def as_uni_field(field):
    """
    Renders a form field like a django-uni-form field::

        {% load uni_form_tags %}
        {{ form.field|as_uni_field }}
    """
    template = get_template('uni_form/field.html')
    c = Context({'field':field})
    return template.render(c)

@register.inclusion_tag("uni_form/includes.html", takes_context=True)
def uni_form_setup(context):
    """
    Creates the `<style>` and `<script>` tags needed to initialize uni-form.

    You can create a local uni-form/includes.html template if you want to customize how
    these files are loaded.
    
    Only works with Django 1.3+
    """
    if 'STATIC_URL' not in context:
        context['STATIC_URL'] = settings.STATIC_URL
    return (context)
