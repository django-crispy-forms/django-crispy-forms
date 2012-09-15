from django.conf import settings
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.safestring import mark_safe

from layout import Layout, LayoutSlice
from utils import render_field, flatatt
from exceptions import FormHelpersException


class DynamicLayoutHandler(object):
    def all(self):
        """
        Returns all layout objects of first level of depth
        """
        return LayoutSlice(self.layout, slice(0, len(self.layout.fields), 1))

    def filter(self, *LayoutClasses, **kwargs):
        """
        Returns a LayoutSlice pointing to layout objects of type `LayoutClass`
        """
        max_level = kwargs.pop('max_level', 0)
        filtered_layout_objects = self.layout.get_layout_objects(LayoutClasses, max_level=max_level)

        return LayoutSlice(self.layout, filtered_layout_objects)

    def filter_by_widget(self, widget_type):
        """
        Returns a LayoutSlice pointing to fields with widgets of `widget_type`
        """
        assert(self.layout is not None and self.form is not None)
        layout_field_names = self.layout.get_field_names()

        # Let's filter all fields with widgets like widget_type
        filtered_fields = []
        for pointer in layout_field_names:
            if isinstance(self.form.fields[pointer[1]].widget, widget_type):
                filtered_fields.append(pointer)

        return LayoutSlice(self.layout, filtered_fields)

    def exclude_by_widget(self, widget_type):
        """
        Returns a LayoutSlice pointing to fields with widgets NOT matching `widget_type`
        """
        assert(self.layout is not None and self.form is not None)
        layout_field_names = self.layout.get_field_names()

        # Let's exclude all fields with widgets like widget_type
        filtered_fields = []
        for pointer in layout_field_names:
            if not isinstance(self.form.fields[pointer[1]].widget, widget_type):
                filtered_fields.append(pointer)

        return LayoutSlice(self.layout, filtered_fields)

    def __getitem__(self, key):
        """
        Return a LayoutSlice that makes changes affect the current instance of the layout
        and not a copy.
        """
        # when key is a string containing the field name
        if isinstance(key, basestring):
            # Django templates access FormHelper attributes using dictionary [] operator
            # This could be a helper['form_id'] access, not looking for a field
            if hasattr(self, key):
                return getattr(self, key)

            assert(self.layout is not None)
            layout_field_names = self.layout.get_field_names()

            filtered_field = []
            for pointer in layout_field_names:
                # There can be an empty pointer
                if len(pointer) == 2 and pointer[1] == key:
                    filtered_field.append(pointer)

            return LayoutSlice(self.layout, filtered_field)

        return LayoutSlice(self.layout, key)


class FormHelper(DynamicLayoutHandler):
    """
    This class controls the form rendering behavior of the form passed to
    the `{% crispy %}` tag. For doing so you will need to set its attributes
    and pass the corresponding helper object to the tag::

        {% crispy form form.helper %}

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

        from crispy_forms.helper import FormHelper
        from crispy_forms.layout import Submit

        class MyForm(forms.Form):
            title = forms.CharField(_("Title"))

            @property
            def helper(self):
                helper = FormHelper()
                helper.form_id = 'this-form-rocks'
                helper.form_class = 'search'
                helper.add_input(Submit('save', 'save'))
                [...]
                return helper

    You can use it in a template doing::

        {% load crispy_forms_tags %}
        {% crispy form %}
    """
    _form_method = 'post'
    _form_action = ''
    _form_style = 'default'
    form = None
    form_id = ''
    form_class = ''
    layout = None
    form_tag = True
    form_error_title = None
    formset_error_title = None
    form_show_errors = True
    render_unmentioned_fields = False
    help_text_inline = False
    error_text_inline = True
    html5_required = False

    def __init__(self, form=None):
        self.attrs = {}
        self.inputs = []

        if form is not None:
            self.form = form
            self.layout = self.build_default_layout(form)

    def build_default_layout(self, form):
        return Layout(*form.fields.keys())

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
        form.rendered_fields = set()

        # This renders the specifed Layout
        html = self.layout.render(form, self.form_style, context)

        if self.render_unmentioned_fields:
            fields = set(form.fields.keys())
            left_fields_to_render = fields - form.rendered_fields
            for field in left_fields_to_render:
                html += render_field(field, form, self.form_style, context)

        # If the user has meta fields defined, not included in the layout
        # we suppose they need to be rendered. Othewise we renderd the
        # layout fields strictly
        if getattr(form, 'Meta', None):
            current_fields = set(getattr(form, 'fields', []))
            left_fields_to_render = current_fields - form.rendered_fields

            for field in left_fields_to_render:
                html += render_field(field, form, self.form_style, context)

        return mark_safe(html)

    def get_attributes(self):
        """
        Used by crispy_forms_tags to get helper attributes
        """
        items = {}
        items['form_method'] = self.form_method.strip()
        items['form_tag'] = self.form_tag
        items['form_style'] = self.form_style.strip()
        items['form_show_errors'] = self.form_show_errors
        items['help_text_inline'] = self.help_text_inline
        items['error_text_inline'] = self.error_text_inline
        items['html5_required'] = self.html5_required

        items['attrs'] = {}
        if self.attrs:
            items['attrs'] = self.attrs.copy()
        if self.form_action:
            items['attrs']['action'] = self.form_action.strip()
        if self.form_id:
            items['attrs']['id'] = self.form_id.strip()
        if self.form_class:
            # uni_form TEMPLATE PACK has a uniForm class by default
            if getattr(settings, 'CRISPY_TEMPLATE_PACK', 'bootstrap') == 'uni_form':
                items['attrs']['class'] = "uniForm %s" % self.form_class.strip()
            else:
                items['attrs']['class'] = self.form_class.strip()
        else:
            if getattr(settings, 'CRISPY_TEMPLATE_PACK', 'bootstrap') == 'uni_form':
                items['attrs']['class'] = self.attrs.get('class', '') + " uniForm"

        items['flat_attrs'] = flatatt(items['attrs'])

        if self.inputs:
            items['inputs'] = self.inputs
        if self.form_error_title:
            items['form_error_title'] = self.form_error_title.strip()
        if self.formset_error_title:
            items['formset_error_title'] = self.formset_error_title.strip()

        for attribute_name, value in self.__dict__.items():
            if attribute_name not in items and attribute_name not in ['layout', 'inputs'] and not attribute_name.startswith('_'):
                items[attribute_name] = value

        return items
