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
        Used to create a Submit button descriptor for the uni_form template tag.
    """
    
    input_type = 'submit'


class Button(BaseInput):
    """
        Used to create a Submit input descriptor for the uni_form template tag.
    """
    
    input_type = 'button'


class Hidden(BaseInput):
    """
        Used to create a Hidden input descriptor for the uni_form template tag.
    """
    
    input_type = 'hidden'

class Reset(BaseInput):
    """
        Used to create a Hidden input descriptor for the uni_form template tag.
    """
    
    input_type = 'reset'

def render_field(field, form):
    if isinstance(field, str):
        return render_form_field(form, field)
    else:
        return field.render(form)

def render_form_field(form, field):
    try:
        field_instance = form.fields[field]
    except KeyError:
        raise Exception("Could not resolve form field '%s'." % field)
    bound_field = BoundField(form, field_instance, field)
    html = render_to_string("uni_form/field.html", {'field': bound_field})
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
    
    layout = Layout(Fieldset('', 'is_company'),
                    Fieldset(_('Contact details'),
                              'email',
                              Row('password1','password2'),
                              'first_name',
                              'last_name',
                              HTML('<img src="/media/somepicture.jpg"/>'),
                              'company',)
    helper.add_layout(layout)
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
        if 'css_class' in args.keys():
            self.css = args['css_class']
        else:
            self.css = None
        self.legend_html = legend and ('<legend>%s</legend><hr/>' % unicode(legend)) or ''
        self.fields = fields
    
    
    def render(self, form):
        if self.css:
            html = u'<fieldset class="%s">' % self.css
        else:
            html = u'<fieldset>'
        html += self.legend_html
        for field in self.fields:
            html += render_field(field, form)
        html += u'</fieldset>'
        return html



class Row(object):
    ''' row container. Renders to a set of <div>'''
    def __init__(self, *fields, **kwargs):
        self.fields = fields
        if 'css_class' in kwargs.keys():
            self.css = kwargs['css_class']
        else:
            self.css = "formRow"
    
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
        if 'css_class' in kwargs.keys():
            self.css = kwargs['css_class']
        else:
            self.css = "formColumn"
    
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
        
        After this in the template:
            
            {% load uni_form %}
            {% uni_form form form.helper %}
        
    
    """
    
    def __init__(self):
        self._form_method = 'POST'
        self._form_action = ''
        self.form_id = ''
        self.form_class = ''
        self.inputs = []
        self.toggle = Toggle()
        self.layout = None
    
    def get_form_method(self):
        return self._form_method
    
    def set_form_method(self, method):
        if method.lower() not in ('get','post'):
            raise FormHelpersException('Only GET and POST are valid in the \
                    form_method helper attribute')
        
        self._form_method = method.upper()
    
    # we set properties the old way because we want to support pre-2.6 python
    form_method = property(get_form_method, set_form_method)
    
    def get_form_action(self):
        return self._form_action
    
    def set_form_action(self, action):
        try:
            self._form_action = reverse(action)
        except NoReverseMatch, e:
            msg = 'Your form action needs to be a named url defined in a urlconf file\n'
            msg += 'Your broken action is: %s\n' % action
            msg += 'NoReverseMatch: %s' % e
            raise FormHelpersException(msg)
    
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
        
