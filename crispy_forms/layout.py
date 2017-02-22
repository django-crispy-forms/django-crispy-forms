from __future__ import unicode_literals

from django.template import Template
from django.template.loader import render_to_string
from django.utils.html import conditional_escape

from crispy_forms.compatibility import string_types, text_type
from crispy_forms.utils import (
    TEMPLATE_PACK, flatatt, get_template_pack, render_field,
)


class TemplateNameMixin(object):

    def get_template_name(self, template_pack):
        if '%s' in self.template:
            template = self.template % template_pack
        else:
            template = self.template

        return template


class LayoutObject(TemplateNameMixin):
    def __getitem__(self, slice):
        return self.fields[slice]

    def __setitem__(self, slice, value):
        self.fields[slice] = value

    def __delitem__(self, slice):
        del self.fields[slice]

    def __len__(self):
        return len(self.fields)

    def __getattr__(self, name):
        """
        This allows us to access self.fields list methods like append or insert, without
        having to declare them one by one
        """
        # Check necessary for unpickling, see #107
        if 'fields' in self.__dict__ and hasattr(self.fields, name):
            return getattr(self.fields, name)
        else:
            return object.__getattribute__(self, name)

    def get_field_names(self, index=None):
        """
        Returns a list of lists, those lists are named pointers. First parameter
        is the location of the field, second one the name of the field. Example::

            [
                [[0,1,2], 'field_name1'],
                [[0,3], 'field_name2']
            ]
        """
        return self.get_layout_objects(string_types, index=None, greedy=True)

    def get_layout_objects(self, *LayoutClasses, **kwargs):
        """
        Returns a list of lists pointing to layout objects of any type matching
        `LayoutClasses`::

            [
                [[0,1,2], 'div'],
                [[0,3], 'field_name']
            ]

        :param max_level: An integer that indicates max level depth to reach when
        traversing a layout.
        :param greedy: Boolean that indicates whether to be greedy. If set, max_level
        is skipped.
        """
        index = kwargs.pop('index', None)
        max_level = kwargs.pop('max_level', 0)
        greedy = kwargs.pop('greedy', False)

        pointers = []

        if index is not None and not isinstance(index, list):
            index = [index]
        elif index is None:
            index = []

        for i, layout_object in enumerate(self.fields):
            if isinstance(layout_object, LayoutClasses):
                if len(LayoutClasses) == 1 and LayoutClasses[0] == string_types:
                    pointers.append([index + [i], layout_object])
                else:
                    pointers.append([index + [i], layout_object.__class__.__name__.lower()])

            # If it's a layout object and we haven't reached the max depth limit or greedy
            # we recursive call
            if hasattr(layout_object, 'get_field_names') and (len(index) < max_level or greedy):
                new_kwargs = {'index': index + [i], 'max_level': max_level, 'greedy': greedy}
                pointers = pointers + layout_object.get_layout_objects(*LayoutClasses, **new_kwargs)

        return pointers

    def get_rendered_fields(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        return ''.join(
            render_field(field, form, form_style, context, template_pack=template_pack, **kwargs)
            for field in self.fields
        )


class Layout(LayoutObject):
    """
    Form Layout. It is conformed by Layout objects: `Fieldset`, `Row`, `Column`, `MultiField`,
    `HTML`, `ButtonHolder`, `Button`, `Hidden`, `Reset`, `Submit` and fields. Form fields
    have to be strings.
    Layout objects `Fieldset`, `Row`, `Column`, `MultiField` and `ButtonHolder` can hold other
    Layout objects within. Though `ButtonHolder` should only hold `HTML` and BaseInput
    inherited classes: `Button`, `Hidden`, `Reset` and `Submit`.

    Example::

        helper.layout = Layout(
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
    """
    def __init__(self, *fields):
        self.fields = list(fields)

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        return self.get_rendered_fields(form, form_style, context, template_pack, **kwargs)


class ButtonHolder(LayoutObject):
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
    template = "%s/layout/buttonholder.html"

    def __init__(self, *fields, **kwargs):
        self.fields = list(fields)
        self.css_class = kwargs.get('css_class', None)
        self.css_id = kwargs.get('css_id', None)
        self.template = kwargs.get('template', self.template)

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        html = self.get_rendered_fields(form, form_style, context, template_pack, **kwargs)

        template = self.get_template_name(template_pack)
        context.update({'buttonholder': self, 'fields_output': html})

        return render_to_string(template, context.flatten())


class BaseInput(TemplateNameMixin):
    """
    A base class to reduce the amount of code in the Input classes.
    """
    template = "%s/layout/baseinput.html"

    def __init__(self, name, value, **kwargs):
        self.name = name
        self.value = value
        self.id = kwargs.pop('css_id', '')
        self.attrs = {}

        if 'css_class' in kwargs:
            self.field_classes += ' %s' % kwargs.pop('css_class')

        self.template = kwargs.pop('template', self.template)
        self.flat_attrs = flatatt(kwargs)

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        """
        Renders an `<input />` if container is used as a Layout object.
        Input button value can be a variable in context.
        """
        self.value = Template(text_type(self.value)).render(context)
        template = self.get_template_name(template_pack)
        context.update({'input': self})

        return render_to_string(template, context.flatten())


class Submit(BaseInput):
    """
    Used to create a Submit button descriptor for the {% crispy %} template tag::

        submit = Submit('Search the Site', 'search this site')

    .. note:: The first argument is also slugified and turned into the id for the submit button.
    """
    input_type = 'submit'

    def __init__(self, *args, **kwargs):
        self.field_classes = 'submit submitButton' if get_template_pack() == 'uni_form' else 'btn btn-primary'
        super(Submit, self).__init__(*args, **kwargs)


class Button(BaseInput):
    """
    Used to create a Submit input descriptor for the {% crispy %} template tag::

        button = Button('Button 1', 'Press Me!')

    .. note:: The first argument is also slugified and turned into the id for the button.
    """
    input_type = 'button'

    def __init__(self, *args, **kwargs):
        self.field_classes = 'button' if get_template_pack() == 'uni_form' else 'btn'
        super(Button, self).__init__(*args, **kwargs)


class Hidden(BaseInput):
    """
    Used to create a Hidden input descriptor for the {% crispy %} template tag.
    """
    input_type = 'hidden'
    field_classes = 'hidden'


class Reset(BaseInput):
    """
    Used to create a Reset button input descriptor for the {% crispy %} template tag::

        reset = Reset('Reset This Form', 'Revert Me!')

    .. note:: The first argument is also slugified and turned into the id for the reset.
    """
    input_type = 'reset'

    def __init__(self, *args, **kwargs):
        self.field_classes = 'reset resetButton' if get_template_pack() == 'uni_form' else 'btn btn-inverse'
        super(Reset, self).__init__(*args, **kwargs)


class Fieldset(LayoutObject):
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
    template = "%s/layout/fieldset.html"

    def __init__(self, legend, *fields, **kwargs):
        self.fields = list(fields)
        self.legend = legend
        self.css_class = kwargs.pop('css_class', '')
        self.css_id = kwargs.pop('css_id', None)
        self.template = kwargs.pop('template', self.template)
        self.flat_attrs = flatatt(kwargs)

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        fields = self.get_rendered_fields(form, form_style, context, template_pack, **kwargs)

        legend = ''
        if self.legend:
            legend = '%s' % Template(text_type(self.legend)).render(context)

        template = self.get_template_name(template_pack)
        return render_to_string(
            template,
            {'fieldset': self, 'legend': legend, 'fields': fields, 'form_style': form_style}
        )


class MultiField(LayoutObject):
    """ MultiField container. Renders to a MultiField <div> """
    template = "%s/layout/multifield.html"
    field_template = "%s/multifield.html"

    def __init__(self, label, *fields, **kwargs):
        self.fields = list(fields)
        self.label_html = label
        self.label_class = kwargs.pop('label_class', 'blockLabel')
        self.css_class = kwargs.pop('css_class', 'ctrlHolder')
        self.css_id = kwargs.pop('css_id', None)
        self.help_text = kwargs.pop('help_text', None)
        self.template = kwargs.pop('template', self.template)
        self.field_template = kwargs.pop('field_template', self.field_template)
        self.flat_attrs = flatatt(kwargs)

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        # If a field within MultiField contains errors
        if context['form_show_errors']:
            for field in map(lambda pointer: pointer[1], self.get_field_names()):
                if field in form.errors:
                    self.css_class += " error"

        field_template = self.field_template % template_pack
        fields_output = self.get_rendered_fields(
            form, form_style, context, template_pack, template=field_template,
            labelclass=self.label_class, layout_object=self, **kwargs
        )

        template = self.get_template_name(template_pack)
        context.update({
            'multifield': self,
            'fields_output': fields_output
        })

        return render_to_string(template, context.flatten())


class Div(LayoutObject):
    """
    Layout object. It wraps fields in a <div>

    You can set `css_id` for a DOM id and `css_class` for a DOM class. Example::

        Div('form_field_1', 'form_field_2', css_id='div-example', css_class='divs')
    """
    template = "%s/layout/div.html"

    def __init__(self, *fields, **kwargs):
        self.fields = list(fields)

        if hasattr(self, 'css_class') and 'css_class' in kwargs:
            self.css_class += ' %s' % kwargs.pop('css_class')
        if not hasattr(self, 'css_class'):
            self.css_class = kwargs.pop('css_class', None)

        self.css_id = kwargs.pop('css_id', '')
        self.template = kwargs.pop('template', self.template)
        self.flat_attrs = flatatt(kwargs)

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        fields = self.get_rendered_fields(form, form_style, context, template_pack, **kwargs)

        template = self.get_template_name(template_pack)
        return render_to_string(template, {'div': self, 'fields': fields})


class Row(Div):
    """
    Layout object. It wraps fields in a div whose default class is "formRow". Example::

        Row('form_field_1', 'form_field_2', 'form_field_3')
    """

    def __init__(self, *args, **kwargs):
        self.css_class = 'formRow' if get_template_pack() == 'uni_form' else 'row'
        super(Row, self).__init__(*args, **kwargs)


class Column(Div):
    """
    Layout object. It wraps fields in a div whose default class is "formColumn". Example::

        Column('form_field_1', 'form_field_2')
    """
    css_class = 'formColumn'


class HTML(object):
    """
    Layout object. It can contain pure HTML and it has access to the whole
    context of the page where the form is being rendered.

    Examples::

        HTML("{% if saved %}Data saved{% endif %}")
        HTML('<input type="hidden" name="{{ step_field }}" value="{{ step0 }}" />')
    """

    def __init__(self, html):
        self.html = html

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        return Template(text_type(self.html)).render(context)


class Field(LayoutObject):
    """
    Layout object, It contains one field name, and you can add attributes to it easily.
    For setting class attributes, you need to use `css_class`, as `class` is a Python keyword.

    Example::

        Field('field_name', style="color: #333;", css_class="whatever", id="field_name")
    """
    template = "%s/field.html"

    def __init__(self, *args, **kwargs):
        self.fields = list(args)

        if not hasattr(self, 'attrs'):
            self.attrs = {}
        else:
            # Make sure shared state is not edited.
            self.attrs = self.attrs.copy()

        if 'css_class' in kwargs:
            if 'class' in self.attrs:
                self.attrs['class'] += " %s" % kwargs.pop('css_class')
            else:
                self.attrs['class'] = kwargs.pop('css_class')

        self.wrapper_class = kwargs.pop('wrapper_class', None)
        self.template = kwargs.pop('template', self.template)

        # We use kwargs as HTML attributes, turning data_id='test' into data-id='test'
        self.attrs.update(dict([(k.replace('_', '-'), conditional_escape(v)) for k, v in kwargs.items()]))

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, extra_context=None, **kwargs):
        if extra_context is None:
            extra_context = {}
        if hasattr(self, 'wrapper_class'):
            extra_context['wrapper_class'] = self.wrapper_class

        template = self.get_template_name(template_pack)

        return self.get_rendered_fields(
            form, form_style, context, template_pack,
            template=template, attrs=self.attrs, extra_context=extra_context,
            **kwargs
        )


class MultiWidgetField(Field):
    """
    Layout object. For fields with :class:`~django.forms.MultiWidget` as `widget`, you can pass
    additional attributes to each widget.

    Example::

        MultiWidgetField(
            'multiwidget_field_name',
            attrs=(
                {'style': 'width: 30px;'},
                {'class': 'second_widget_class'}
            ),
        )

    .. note:: To override widget's css class use ``class`` not ``css_class``.
    """
    def __init__(self, *args, **kwargs):
        self.fields = list(args)
        self.attrs = kwargs.pop('attrs', {})
        self.template = kwargs.pop('template', self.template)
