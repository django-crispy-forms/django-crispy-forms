"""
    Utilities for helping developers use python for adding various attributes,
    elements, and UI elements to forms generated via the uni_form template tag.

"""
from django.core.urlresolvers import reverse, NoReverseMatch
from django.forms.forms import BoundField
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


from uni_form.util import BaseInput, Toggle

class FormHelpersException(Exception):
    """ This is raised when building a form via helpers throws an error.
        We want to catch form helper errors as soon as possible because
        debugging templatetags is never fun.
    """
    pass


class Submit(BaseInput):
    """
        Used to create a Submit button descriptor for the uni_form template tag:
            
            submit = Submit('Search the Site','search this site')
        
        Note: The first argument is also slugified and turned into the id for the submit button.
    
    """
    
    input_type = 'submit'
    field_classes = 'submit submitButton'


class Button(BaseInput):
    """
        Used to create a Submit input descriptor for the uni_form template tag:
            
            button = Button('Button 1','Press Me!')
        
        Note: The first argument is also slugified and turned into the id for the button.
    """
    
    input_type = 'button'
    field_classes = 'button'

class Hidden(BaseInput):
    """
        Used to create a Hidden input descriptor for the uni_form template tag.
    """
    
    input_type = 'hidden'
    field_classes = 'hidden'

class Reset(BaseInput):
    """
        Used to create a Hidden input descriptor for the uni_form template tag.
            
            reset = Reset('Reset This Form','Revert Me!')
        
        Note: The first argument is also slugified and turned into the id for the reset.
    
    """
    
    input_type = 'reset'
    field_classes = 'reset resetButton'

def render_field(field, form, template="uni_form/field.html", labelclass=None):
    if not isinstance(field, str):
        return field.render(form)

    try:
        field_instance = form.fields[field]
    except KeyError:
        raise Exception("Could not resolve form field '%s'." % field)
    bound_field = BoundField(form, field_instance, field)
    html = render_to_string(template, {'field': bound_field, 'labelclass': labelclass})
    if not hasattr(form, 'rendered_fields'):
        form.rendered_fields = []
    if not field in form.rendered_fields:
        form.rendered_fields.append(field)
    else:
        raise Exception("A field should only be rendered once: %s" % field)
    return html

class Layout(object):
    '''
    Form Layout, add fieldsets, rows, fields and html
    
    example:
    
    >>> layout = Layout(Fieldset('', 'is_company'),
    ...     Fieldset(_('Contact details'),
    ...         'email',
    ...         Row('password1','password2'),
    ...         'first_name',
    ...         'last_name',
    ...         HTML('<img src="/media/somepicture.jpg"/>'),
    ...         'company'))
    >>> helper.add_layout(layout)
    '''
    def __init__(self, *fields):
        self.fields = fields
    
    def render(self, form):
        html = ""
        for field in self.fields:
            html += render_field(field, form)
        for field in form.fields.keys():
            if not field in form.rendered_fields:
                html += render_field(field, form)
        return html

class Fieldset(object):
    
    ''' Fieldset container. Renders to a <fieldset>. '''
    
    def __init__(self, legend, *fields, **args):
        self.css = args.get('css_class', None)
        self.legend = legend
        self.fields = fields

    
    def render(self, form):
        if self.css:
            html = u'<fieldset class="%s">' % self.css
        else:
            html = u'<fieldset>'
        html += self.legend and (u'<legend>%s</legend>' % self.legend) or ''
        for field in self.fields:
            html += render_field(field, form)
        html += u'</fieldset>'
        return html



class MultiField(object):
    ''' multiField container. Renders to a multiField <div> '''

    def __init__(self, label, *fields, **kwargs):
        #TODO: Decide on how to support css classes for both container divs
        self.div_class = kwargs.get('css_class', u'ctrlHolder')
        self.label_class = kwargs.get('label_class', u'blockLabel')
        self.label_html = label and (u'<p class="label">%s</p>\n' % unicode(label)) or ''
        self.fields = fields

    def render(self, form):
        fieldoutput = u''
        errors = u''
        helptext = u''
        count = 0
        for field in self.fields:
            fieldoutput += render_field(field, form, 'uni_form/multifield.html', self.label_class)
            try:
                field_instance = form.fields[field]
            except KeyError:
                raise Exception("Could not resolve form field '%s'." % field)
            bound_field = BoundField(form, field_instance, field)
            auto_id = bound_field.auto_id
            for error in bound_field.errors:
                errors += u'<p id="error_%i_%s" class="errorField">%s</p>' % (count, auto_id, error)
                count += 1
            if bound_field.help_text:
                helptext += u'<p id="hint_%s" class="formHint">%s</p>' % (auto_id, bound_field.help_text)

        if errors:
            self.css += u' error'

        output = u'<div class="%s">\n' % self.div_class
        output += errors
        output += self.label_html
        output += u'<div class="multiField">\n'
        output += fieldoutput
        output += u'</div>\n'
        output += helptext
        output += u'</div>\n'
        return output



class Row(object):
    ''' row container. Renders to a set of <div>'''
    def __init__(self, *fields, **kwargs):
        self.fields = fields
        self.css = kwargs.get('css_class', u'formRow')

    def render(self, form):
        output = u'<div class="%s">' % self.css
        for field in self.fields:
            output += render_field(field, form)
        output += u'</div>'
        return u''.join(output)


class Column(object):
    ''' column container. Renders to a set of <div>'''
    def __init__(self, *fields, **kwargs):
        self.fields = fields
        self.css = kwargs.get('css_class', u'formColumn')

    def render(self, form):
        output = u'<div class="%s">' % self.css
        for field in self.fields:
            output += render_field(field, form)
        output += u'</div>'
        return u''.join(output)


class HTML(object):
    
    ''' HTML container '''
    
    def __init__(self, html):
        self.html = unicode(html)
    
    def render(self, form):
        return self.html


class FormHelper(object):
    """
        By setting attributes to me you can easily create the text that goes
        into the uni_form template tag. One use case is to add to your form
        class.
        
        Special attribute behavior:
            
            method: Defaults to POST but you can also do 'GET'
            
            form_action: applied to the form action attribute. Can be a named url in
                your urlconf that can be executed via the *url* default template tag or can
                simply point to another URL.
            
            id: Generates a form id for dom identification.
                If no id provided then no id attribute is created on the form.
            
            class: add space seperated classes to the class list.
                Defaults to uniForm.
                Always starts with uniForm even do specify classes.
            
            form_tag: Defaults to True. If set to False it renders the form without the form tags.
            
            use_csrf_protection: Defaults to True. If set to True a CSRF protection token is
                rendered in the form. This should only be set as False for forms targeting
                external sites or internal sites without CSRF protection (as described in the
                Django documentation).
                Requires the presence of a csrf token in the current context with the identifier
                "csrf_token" (which is automatically added to your context when using RequestContext).

        
        Demonstration:
            
            First we create a MyForm class and instantiate it
            
            >>> from django import forms
            >>> from uni_form.helpers import FormHelper, Submit, Reset
            >>> from django.utils.translation import ugettext_lazy as _
            >>> class MyForm(forms.Form):
            ...     title = forms.CharField(label=_("Title"), max_length=30, widget=forms.TextInput())
            ...     # this displays how to attach a formHelper to your forms class.
            ...     helper = FormHelper()
            ...     helper.form_id = 'this-form-rocks'
            ...     helper.form_class = 'search'
            ...     submit = Submit('search','search this site')
            ...     helper.add_input(submit)
            ...     reset = Reset('reset','reset button')
            ...     helper.add_input(reset)
            
            After this in the template::
                
                {% load uni_form_tags %}
                {% uni_form form form.helper %}

    
    """
    _form_method = 'post'
    _form_action = ''
    form_id = ''
    form_class = ''
    inputs = []
    layout = None
    form_tag = True
    use_csrf_protection = True

    
    def __init__(self):
        
        self.inputs = self.inputs[:]
        self.toggle = Toggle()
    
    def get_form_method(self):
        return self._form_method
    
    def set_form_method(self, method):
        if method.lower() not in ('get','post'):
            raise FormHelpersException('Only GET and POST are valid in the \
                    form_method helper attribute')
        
        self._form_method = method.lower()
    
    # we set properties the old way because we want to support pre-2.6 python
    form_method = property(get_form_method, set_form_method)
    
    def get_form_action(self):
        try:
            return reverse(self._form_action)
        except NoReverseMatch:
            return self._form_action

    def set_form_action(self, action):
        self._form_action = action
    
    # we set properties the old way because we want to support pre-2.6 python
    form_action = property(get_form_action, set_form_action)
    
    def add_input(self, input_object):
        self.inputs.append(input_object)
    
    def add_layout(self, layout):
        self.layout = layout
    
    def render_layout(self, form):
        return mark_safe(self.layout.render(form))
    
    def get_attr(self):
        items = {}
        items['form_method'] = self.form_method.strip()
        items['form_tag'] = self.form_tag
        items['use_csrf_protection'] = self.use_csrf_protection
        
        if self.form_action:
            items['form_action'] = self.form_action.strip()
        if self.form_id:
            items['id'] = self.form_id.strip()
        if self.form_class:
            items['class'] = self.form_class.strip()
        if self.inputs:
            items['inputs'] = self.inputs
        if self.toggle.fields:
            items['toggle_fields'] = self.toggle.fields
        return items

