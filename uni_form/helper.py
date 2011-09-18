from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.safestring import mark_safe

from utils import render_field


class FormHelpersException(Exception):
    """ 
    This is raised when building a form via helpers throws an error.
    We want to catch form helper errors as soon as possible because
    debugging templatetags is never fun.
    """
    pass


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
        form.rendered_fields = []
        
        html = self.layout.render(form, self.form_style, context)

        for field in form.fields.keys():
            if not field in form.rendered_fields:
                html += render_field(field, form, self.form_style, context)

        return mark_safe(html)
    
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
