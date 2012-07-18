import itertools

from django.conf import settings
from django.template import Context, Template
from django.template.loader import render_to_string
from django.utils.html import conditional_escape

from utils import render_field, flatatt

TEMPLATE_PACK = getattr(settings, 'CRISPY_TEMPLATE_PACK', 'bootstrap')


class LayoutObject(object):
    def __getitem__(self, slice):
        return self.fields[slice]

    def __setitem__(self, slice, value):
        self.fields[slice] = value

    def append(self, value):
        self.fields.append(value)

    def get_field_names(self, index=None):
        """
        Returns a list of lists, those lists are pointers to field names. First parameter
        is the location of the field, second one the name of the field. Example::

            [
               [[0,1,2], 'field_name1'], [[0,3], 'field_name2']
            ]
        """
        field_names = []

        if index is not None and not isinstance(index, list):
            index = [index]
        elif index is None:
            index = []

        # The layout object contains other layout objects
        if not all([isinstance(layout_object, basestring) for layout_object in self.fields]):
            for i, layout_object in enumerate(self.fields):
                # If it's a layout object, we recursive call
                if not isinstance(layout_object, basestring):
                    if hasattr(layout_object, 'get_field_names'):
                        field_names.append(layout_object.get_field_names(index + [i]))
                # If it's a string, then it's a basic case
                else:
                    field_names.append([index + [i], layout_object])

            if len(field_names) == 1:
                return field_names[0]
            else:
                return field_names

        # Base case: It only contains field_names
        else:
            fields_to_return = []
            for i, field_name in enumerate(self.fields):
                fields_to_return.append([index + [i], field_name])
            return list(itertools.chain.from_iterable(fields_to_return))


class Layout(LayoutObject):
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
        html = ""
        for field in self.fields:
            html += render_field(field, form, form_style, context)
        return html


class LayoutSlice(object):
    def __init__(self, layout, key):
        self.layout = layout
        if isinstance(key, (int, long)):
            self.slice = slice(key, key+1, 1)
        else:
            self.slice = key

    def wrap(self, LayoutClass, **kwargs):
        if isinstance(self.slice, slice):
            for i in range(*self.slice.indices(len(self.layout.fields))):
                self.layout.fields[i] = LayoutClass(self.layout.fields[i], **kwargs)

        elif isinstance(self.slice, list):
            # filter returns a list of integers
            for pointer in self.slice:
                if isinstance(pointer, int):
                    self.layout.fields[pointer] = LayoutClass(self.layout.fields[pointer], **kwargs)
                else:
                    pos = pointer[0]
                    layout_object = self.layout.fields[pos[0]]
                    for i in pointer[0][1:-1]:
                        layout_object = layout_object.fields[i]

                    layout_object.fields[pos[-1]] = LayoutClass(layout_object.fields[pos[-1]], **kwargs)




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
    template = "uni_form/layout/buttonholder.html"

    def __init__(self, *fields, **kwargs):
        self.fields = list(fields)
        self.css_class = kwargs.get('css_class', None)
        self.css_id = kwargs.get('css_id', None)
        self.template = kwargs.get('template', self.template)

    def render(self, form, form_style, context):
        html = u''
        for field in self.fields:
            html += render_field(field, form, form_style, context)

        return render_to_string(self.template, Context({'buttonholder': self, 'fields_output': html}))


class BaseInput(object):
    """
    A base class to reduce the amount of code in the Input classes.
    """
    template = "uni_form/layout/baseinput.html"

    def __init__(self, name, value, **kwargs):
        self.name = name
        self.value = value
        self.id = kwargs.get('css_id', '')
        self.attrs = {}

        if kwargs.has_key('css_class'):
            self.field_classes += ' %s' % kwargs.pop('css_class')

        self.template = kwargs.pop('template', self.template)
        self.flat_attrs = flatatt(kwargs)

    def render(self, form, form_style, context):
        """
        Renders an `<input />` if container is used as a Layout object
        """
        return render_to_string(self.template, Context({'input': self}))


class Submit(BaseInput):
    """
    Used to create a Submit button descriptor for the {% crispy %} template tag::

        submit = Submit('Search the Site', 'search this site')

    .. note:: The first argument is also slugified and turned into the id for the submit button.
    """
    input_type = 'submit'
    field_classes = 'submit submitButton' if TEMPLATE_PACK == 'uni_form' else 'btn'


class Button(BaseInput):
    """
    Used to create a Submit input descriptor for the {% crispy %} template tag::

        button = Button('Button 1', 'Press Me!')

    .. note:: The first argument is also slugified and turned into the id for the button.
    """
    input_type = 'button'
    field_classes = 'button'


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
    field_classes = 'reset resetButton'


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
    template = "uni_form/layout/fieldset.html"

    def __init__(self, legend, *fields, **kwargs):
        self.fields = list(fields)
        self.legend = unicode(legend)
        self.css_class = kwargs.pop('css_class', '')
        self.css_id = kwargs.pop('css_id', None)
        # Overrides class variable with an instance level variable
        self.template = kwargs.pop('template', self.template)
        self.flat_attrs = flatatt(kwargs)

    def render(self, form, form_style, context):
        fields = ''
        for field in self.fields:
            fields += render_field(field, form, form_style, context)

        legend = ''
        if self.legend:
            legend = u'%s' % Template(self.legend).render(context)
        return render_to_string(self.template, Context({'fieldset': self, 'legend': legend, 'fields': fields, 'form_style': form_style}))


class MultiField(LayoutObject):
    """ multiField container. Renders to a multiField <div> """
    template = "uni_form/layout/multifield.html"

    def __init__(self, label, *fields, **kwargs):
        #TODO: Decide on how to support css classes for both container divs
        self.fields = list(fields)
        self.label_html = unicode(label)
        self.label_class = kwargs.pop('label_class', u'blockLabel')
        self.css_class = kwargs.pop('css_class', u'ctrlHolder')
        self.css_id = kwargs.pop('css_id', None)
        self.template = kwargs.pop('template', self.template)
        self.flat_attrs = flatatt(kwargs)

    def render(self, form, form_style, context):
        if form.errors:
            self.css_class += " error"

        # We need to render fields using django-uni-form render_field so that MultiField can
        # hold other Layout objects inside itself
        fields_output = u''
        self.bound_fields = []
        for field in self.fields:
            fields_output += render_field(field, form, form_style, context, 'uni_form/multifield.html', self.label_class, layout_object=self)

        return render_to_string(self.template, Context({'multifield': self, 'fields_output': fields_output}))


class Div(LayoutObject):
    """
    Layout object. It wraps fields in a <div>

    You can set `css_id` for a DOM id and `css_class` for a DOM class. Example::

        Div('form_field_1', 'form_field_2', css_id='div-example', css_class='divs')
    """
    template = "uni_form/layout/div.html"

    def __init__(self, *fields, **kwargs):
        self.fields = list(fields)

        if hasattr(self, 'css_class') and kwargs.has_key('css_class'):
            self.css_class += ' %s' % kwargs.pop('css_class')
        if not hasattr(self, 'css_class'):
            self.css_class = kwargs.pop('css_class', None)

        self.css_id = kwargs.pop('css_id', '')
        self.template = kwargs.pop('template', self.template)
        self.flat_attrs = flatatt(kwargs)

    def render(self, form, form_style, context):
        fields = ''
        for field in self.fields:
            fields += render_field(field, form, form_style, context)

        return render_to_string(self.template, Context({'div': self, 'fields': fields}))


class Row(Div):
    """
    Layout object. It wraps fields in a div whose default class is "formRow". Example::

        Row('form_field_1', 'form_field_2', 'form_field_3')
    """
    css_class = 'formRow'


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
        self.html = unicode(html)

    def render(self, form, form_style, context):
        return Template(self.html).render(context)


class Field(LayoutObject):
    """
    Layout object, It contains one field name, and you can add attributes to it easily.
    For setting class attributes, you need to use `css_class`, as `class` is a Python keyword.

    Example::

        Field('field_name', style="color: #333;", css_class="whatever", id="field_name")
    """
    template = "%s/field.html" % TEMPLATE_PACK

    def __init__(self, *args, **kwargs):
        self.fields = list(args)

        if not hasattr(self, 'attrs'):
            self.attrs = {}

        if kwargs.has_key('css_class'):
            if 'class' in self.attrs:
                self.attrs['class'] += " %s" % kwargs.pop('css_class')
            else:
                self.attrs['class'] = kwargs.pop('css_class')

        self.template = kwargs.pop('template', self.template)

        # We use kwargs as HTML attributes, turning data_id='test' into data-id='test'
        self.attrs.update(dict([(k.replace('_', '-'), conditional_escape(v)) for k,v in kwargs.items()]))

    def render(self, form, form_style, context):
        html = ''
        for field in self.fields:
            html += render_field(field, form, form_style, context, template=self.template, attrs=self.attrs)
        return html

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


class UneditableField(Field):
    """
    Layout object for rendering fields as uneditable in bootstrap

    Example::

        UneditableField('field_name', css_class="input-xlarge")
    """
    template = "bootstrap/layout/uneditable_input.html"

    def __init__(self, field, *args, **kwargs):
        self.attrs = {'class': 'uneditable-input'}
        super(UneditableField, self).__init__(field, *args, **kwargs)
