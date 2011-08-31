"""
    Utilities for helping developers use python for adding various attributes,
    elements, and UI elements to forms generated via the uni_form template tag.

"""
import logging
import sys

from django.conf import settings
from django.core.urlresolvers import reverse, NoReverseMatch
from django.forms.forms import BoundField
from django.template import Context, Template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class FormHelpersException(Exception):
    """ 
    This is raised when building a form via helpers throws an error.
    We want to catch form helper errors as soon as possible because
    debugging templatetags is never fun.
    """
    pass


class ButtonHolder(object):
    """
    Layout object. It wraps fields in a <div class="buttonHolder">

    This is where you should put Layout objects that render to form buttons like Submit. 
    It should only hold `HTML` and `BaseInput` inherited objects.

    Example::
        
        ButtonHolder(
            HTML(<span style="display: hidden;">Information Saved</span>),
            Submit('Save', 'Save')
        )
    """
    def __init__(self, *fields, **kwargs):
        self.fields = list(fields)
        self.css_class = kwargs.get('css_class', None)
        self.css_id = kwargs.get('css_id', None)

    def render(self, form, form_style, context):
        html = u'<div '
        if self.css_id:
            html += u'id="%s" ' % self.css_id
        if self.css_class:
            html += u'class="buttonHolder %s">' % self.css_class
        else:
            html += u'class="buttonHolder">'

        for field in self.fields:
            html += render_field(field, form, form_style, context)

        html += u'</div>'
        return html


class BaseInput(object):
    """
    A base class to reduce the amount of code in the Input classes.
    """
    def __init__(self, name, value, **kwargs):
        self.name = name
        self.value = value
        
        if kwargs.has_key('css_class'):
            self.field_classes += ' %s' % kwargs.get('css_class')
        
    def render(self, form, form_style, context):
        """
        Renders an `<input />` if container is used as a Layout object
        """
        template = Template("""
            <input type="{{ input.input_type }}"
                   name="{{ input.name|slugify }}"
                   value="{{ input.value }}"
                   {% ifnotequal input.input_type "hidden" %}
                        class="{{ input.field_classes }}"
                        id="{{ input.input_type }}-id-{{ input.name|slugify }}"
                   {% endifnotequal %}/>
        """)
       
        c = Context({'input': self})
        return template.render(c)


class Submit(BaseInput):
    """
    Used to create a Submit button descriptor for the uni_form template tag::
    
        submit = Submit('Search the Site', 'search this site')
    
    .. note:: The first argument is also slugified and turned into the id for the submit button.
    """
    input_type = 'submit'
    field_classes = 'submit submitButton'


class Button(BaseInput):
    """
    Used to create a Submit input descriptor for the uni_form template tag::

        button = Button('Button 1', 'Press Me!')
    
    .. note:: The first argument is also slugified and turned into the id for the button.
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
    Used to create a Hidden input descriptor for the uni_form template tag::
    
        reset = Reset('Reset This Form', 'Revert Me!')
    
    .. note:: The first argument is also slugified and turned into the id for the reset.
    """
    input_type = 'reset'
    field_classes = 'reset resetButton'


def render_field(field, form, form_style, context, template="uni_form/field.html", labelclass=None):
    """
    Renders a field, if the field is a django-uni-form object like a `Row` or a 
    `Fieldset`, calls its render method. The field is added to a list that the form 
    holds called `rendered_fields` to avoid double rendering fields. If the field is 
    a form field a `BoundField` is instantiated, rendered and its html returned.
    """
    FAIL_SILENTLY = getattr(settings, 'UNIFORM_FAIL_SILENTLY', True)

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
    except KeyError:
        if not FAIL_SILENTLY:
            raise Exception("Could not resolve form field '%s'." % field)
        else:
            field_instance = None
            logging.warning("Could not resolve form field '%s'." % field, exc_info=sys.exc_info())
            
    if not field in form.rendered_fields:
        form.rendered_fields.append(field)
    else:
        if not FAIL_SILENTLY:
            raise Exception("A field should only be rendered once: %s" % field)
        else:
            logging.warning("A field should only be rendered once: %s" % field, exc_info=sys.exc_info())

    if field_instance is None:
        html = ''
    else:
        bound_field = BoundField(form, field_instance, field)
        html = render_to_string(template, {'field': bound_field, 'labelclass': labelclass})

    return html


class Layout(object):
    """ 
    Form Layout. It is conformed by Layout objects: `Fieldset`, `Row`, `Column`, `MultiField`,
    `HTML`, `ButtonHolder`, `Button`, `Hidden`, `Reset`, `Submit` and fields. Form fields 
    have to be strings.
    
    Layout objects `Fieldset`, `Row`, `Column`, `MultiField` and `ButtonHolder` can hold other 
    Layout objects within. Though `ButtonHolder` should only hold `HTML` and BaseInput 
    inherited classes: `Button`, `Hidden`, `Reset` and `Submit`.
    
    You need to add your `Layout` to the `FormHelper` using its method `add_layout`.

    Example::

        layout = Layout(
            Fieldset('Company data', 
                'is_company'
            ),
            Fieldset(_('Contact details'),
                'email',
                Row('password1', 'password2'),
                'first_name',
                'last_name',
                HTML('<img src="/media/somepicture.jpg"/>'),
                'company'
            ),
            ButtonHolder(
                Submit('Save', 'Save', css_class='button white'),
            ),
        )
        
        helper.add_layout(layout)
    """
    def __init__(self, *fields):
        self.fields = list(fields)
    
    def render(self, form, form_style, context):
        form.rendered_fields = []
        html = ""
        for field in self.fields:
            html += render_field(field, form, form_style, context)
        for field in form.fields.keys():
            if not field in form.rendered_fields:
                html += render_field(field, form, form_style, context)
        return html


class Fieldset(object):
    """ 
    Layout object. It wraps fields in a <fieldset> 
    
    Example::

        Fieldset("Text for the legend",
            'form_field_1',
            'form_field_2'
        )

    The first parameter is the text for the fieldset legend. This text is context aware,
    so you can do things like::
    
        Fieldset("Data for {{ user.username }}",
            'form_field_1',
            'form_field_2'
        )
    """

    def __init__(self, legend, *fields, **kwargs):
        self.css_class = kwargs.get('css_class', None)
        self.css_id = kwargs.get('css_id', None)
        self.legend = Template(legend)
        self.fields = list(fields)
    
    def render(self, form, form_style, context):
        html = u'<fieldset'
        if self.css_id:
            html += u' id="%s"' % self.css_id
        if self.css_class:
            html += u' class="%s %s"' % (self.css_class, form_style)
        else:
            html += u' class="%s"' % form_style
        html += '>'

        html += self.legend and (u'<legend>%s</legend>' % self.legend.render(context)) or ''
        for field in self.fields:
            html += render_field(field, form, form_style, context)
        html += u'</fieldset>'
        return html


class MultiField(object):
    """ multiField container. Renders to a multiField <div> """

    def __init__(self, label, *fields, **kwargs):
        #TODO: Decide on how to support css classes for both container divs
        self.div_class = kwargs.get('css_class', u'ctrlHolder')
        self.div_id = kwargs.get('css_id', None)
        self.label_class = kwargs.get('label_class', u'blockLabel')
        self.label_html = label and (u'<p class="label">%s</p>\n' % unicode(label)) or ''
        self.fields = fields

    def render(self, form, form_style, context):
        FAIL_SILENTLY = getattr(settings, 'UNIFORM_FAIL_SILENTLY', True)

        fieldoutput = u''
        errors = u''
        helptext = u''
        count = 0
        for field in self.fields:
            fieldoutput += render_field(field, form, form_style, context, 'uni_form/multifield.html', self.label_class)
            try:
                field_instance = form.fields[field]
            except KeyError:
                if not FAIL_SILENTLY:
                    raise Exception("Could not resolve form field '%s'." % field)
                else:
                    logging.warning("Could not resolve form field '%s'." % field, exc_info=sys.exc_info())
                    continue

            bound_field = BoundField(form, field_instance, field)
            auto_id = bound_field.auto_id
            for error in bound_field.errors:
                errors += u'<p id="error_%i_%s" class="errorField">%s</p>' % (count, auto_id, error)
                count += 1
            if bound_field.help_text:
                helptext += u'<p id="hint_%s" class="formHint">%s</p>' % (auto_id, bound_field.help_text)

        if errors:
            self.css += u' error'

        output = u'<div'
        if self.div_id:
            output += u' id="%s"' % self.div_id
        output += u' class="%s"' % self.div_class
        output += '>\n'
        output += errors
        output += self.label_html
        output += u'<div class="multiField">\n'
        output += fieldoutput
        output += u'</div>\n'
        output += helptext
        output += u'</div>\n'
        return output


class Row(object):
    """ 
    Layout object. It wraps fields in a div whose default class is "formRow". 

    Example::

        Row('form_field_1', 'form_field_2', 'form_field_3')
    """

    def __init__(self, *fields, **kwargs):
        self.fields = fields
        self.css_class = kwargs.get('css_class', u'formRow')
        self.css_id = kwargs.get('css_id', u'')

    def render(self, form, form_style, context):
        output = u'<div'
        if self.css_id:
            output += u' id="%s"' % self.css_id
        if self.css_class:
            output += u' class="%s"' % self.css_class
        output += '>'

        for field in self.fields:
            output += render_field(field, form, form_style, context)

        output += u'</div>'
        return u''.join(output)


class Column(object):
    """ 
    Layout object. It wraps fields in a div whose default class is "formColumn".
    
    Example::

        Column('form_field_1', 'form_field_2') 
    """
    
    def __init__(self, *fields, **kwargs):
        self.fields = fields
        self.css_class = kwargs.get('css_class', u'formColumn')
        self.css_id = kwargs.get('css_id', u'')

    def render(self, form, form_style, context):
        output = u'<div'
        if self.css_id:
            output += u' id="%s"' % self.css_id
        if self.css_class:
            output += u' class="%s"' % self.css_class
        output += '>'

        for field in self.fields:
            output += render_field(field, form, form_style, context)

        output += u'</div>'
        return u''.join(output)


class HTML(object):
    """ 
    Layout object. It can contain pure HTML and it has access to the whole
    context of the page where the form is being rendered.
    
    Examples::

        HTML("{% if saved %}Data saved{% endif %}")
        HTML('<input type="hidden" name="{{ step_field }}" value="{{ step0 }}" />')
    """
    
    def __init__(self, html):
        self.html = unicode(html)
    
    def render(self, form, form_style, context):
        return Template(self.html).render(context)


class FormHelper(object):
    """
    This class controls the form rendering behavior of the form passed to 
    the `{% uni_form %}` tag. For doing so you will need to set its attributes
    and pass the corresponding helper object to the tag::

        {% uni_form form form.helper %}
   
    Let's see what attributes you can set and what form behaviors they apply to:
        
        **form_method**: Specifies form method attribute.
            You can see it to 'POST' or 'GET'. Defaults to 'POST'
        
        **form_action**: Applied to the form action attribute:
            - Can be a named url in your URLconf that can be executed via the `{% url %}` template tag. \
            Example: 'show_my_profile'. In your URLconf you could have something like::

                url(r'^show/profile/$', 'show_my_profile_view', name = 'show_my_profile')

            - It can simply point to a URL '/whatever/blabla/'.
       
        **form_id**: Generates a form id for dom identification.
            If no id provided then no id attribute is created on the form.
        
        **form_class**: String containing separated CSS clases to be applied 
            to form class attribute. The form will always have by default
            'uniForm' class.
        
        **form_tag**: It specifies if <form></form> tags should be rendered when using a Layout. 
            If set to False it renders the form without the <form></form> tags. Defaults to True.
        
        **form_error_title**: If a form has `non_field_errors` to display, they 
            are rendered in a div. You can set title's div with this attribute.
            Example: "Oooops!" or "Form Errors"

        **formset_error_title**: If a formset has `non_form_errors` to display, they 
            are rendered in a div. You can set title's div with this attribute.
    
        **form_style**: Uni-form has two built in different form styles. You can choose
            your favorite. This can be set to "default" or "inline". Defaults to "default".

    Public Methods:
        
        **add_input(input)**: You can add input buttons using this method. Inputs
            added using this method will be rendered at the end of the form/formset.

        **add_layout(layout)**: You can add a `Layout` object to `FormHelper`. The Layout
            specifies in a simple, clean and DRY way how the form fields should be rendered.
            You can wrap fields, order them, customize pretty much anything in the form.

    Best way to add a helper to a form is adding a property named helper to the form 
    that returns customized `FormHelper` object::

        from uni_form import helpers

        class MyForm(forms.Form):
            title = forms.CharField(_("Title"))

            @property
            def helper(self):
                helper = helpers.FormHelper()
                helper.form_id = 'this-form-rocks'
                helper.form_class = 'search'
                submit = helpers.Submit('submit','Submit')
                helper.add_input(submit)
                [...]
                return helper

    You can use it in a template doing::
        
        {% load uni_form_tags %}
        <html>
            <body>
                <div id="where-I-want-the-generated-form">
                    {% uni_form form form.helper %}
                </div>
            </body>            
        </html>
    """
    _form_method = 'post'
    _form_action = ''
    _form_style = 'default'
    form_id = ''
    form_class = ''
    inputs = []
    layout = None
    form_tag = True
    form_error_title = None
    formset_error_title = None

    def __init__(self):
        self.inputs = self.inputs[:]
 
    def get_form_method(self):
        return self._form_method
    
    def set_form_method(self, method):
        if method.lower() not in ('get', 'post'):
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

    def get_form_style(self):
        if self._form_style == "default":
            return ''

        if self._form_style == "inline":
            return 'inlineLabels'
    
    def set_form_style(self, style):
        if style.lower() not in ('default', 'inline'):
            raise FormHelpersException('Only default and inline are valid in the \
                    form_style helper attribute')
        
        self._form_style = style.lower()
    
    form_style = property(get_form_style, set_form_style)
   
    def add_input(self, input_object):
        self.inputs.append(input_object)
    
    def add_layout(self, layout):
        self.layout = layout
    
    def render_layout(self, form, context):
        """
        Returns safe html of the rendering of the layout
        """
        return mark_safe(self.layout.render(form, self.form_style, context))
    
    def get_attributes(self):
        """
        Used by the uni_form_tags to get helper attributes
        """
        items = {}
        items['form_method'] = self.form_method.strip()
        items['form_tag'] = self.form_tag
        items['form_style'] = self.form_style.strip()
        
        if self.form_action:
            items['form_action'] = self.form_action.strip()
        if self.form_id:
            items['id'] = self.form_id.strip()
        if self.form_class:
            items['class'] = self.form_class.strip()
        if self.inputs:
            items['inputs'] = self.inputs
        if self.form_error_title:
            items['form_error_title'] = self.form_error_title.strip()
        if self.formset_error_title:
            items['formset_error_title'] = self.formset_error_title.strip()
        return items
