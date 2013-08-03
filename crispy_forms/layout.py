import warnings

from django.conf import settings
from django.template import Context, Template
from django.template.loader import render_to_string
from django.utils.html import conditional_escape

from crispy_forms.compatibility import string_types, text_type
from crispy_forms.utils import render_field, flatatt

TEMPLATE_PACK = getattr(settings, 'CRISPY_TEMPLATE_PACK', 'bootstrap')


class LayoutObject(object):
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
        having to declaee them one by one
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
        return self.get_layout_objects(string_types, greedy=True)

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

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):
        html = ""
        for field in self.fields:
            html += render_field(
                field,
                form,
                form_style,
                context,
                template_pack=template_pack
            )
        return html


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

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):
        html = u''
        for field in self.fields:
            html += render_field(field, form, form_style,
                                 context, template_pack=template_pack)

        return render_to_string(self.template, Context({'buttonholder': self, 'fields_output': html}))


class BaseInput(object):
    """
    A base class to reduce the amount of code in the Input classes.
    """
    template = "%s/layout/baseinput.html" % TEMPLATE_PACK

    def __init__(self, name, value, **kwargs):
        self.name = name
        self.value = value
        self.id = kwargs.pop('css_id', '')
        self.attrs = {}

        if 'css_class' in kwargs:
            self.field_classes += ' %s' % kwargs.pop('css_class')

        self.template = kwargs.pop('template', self.template)
        self.flat_attrs = flatatt(kwargs)

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):
        """
        Renders an `<input />` if container is used as a Layout object.
        Input button value can be a variable in context.
        """
        self.value = Template(text_type(self.value)).render(context)
        return render_to_string(self.template, Context({'input': self}))


class Submit(BaseInput):
    """
    Used to create a Submit button descriptor for the {% crispy %} template tag::

        submit = Submit('Search the Site', 'search this site')

    .. note:: The first argument is also slugified and turned into the id for the submit button.
    """
    input_type = 'submit'
    field_classes = 'submit submitButton' if TEMPLATE_PACK == 'uni_form' else 'btn btn-primary'


class Button(BaseInput):
    """
    Used to create a Submit input descriptor for the {% crispy %} template tag::

        button = Button('Button 1', 'Press Me!')

    .. note:: The first argument is also slugified and turned into the id for the button.
    """
    input_type = 'button'
    field_classes = 'button' if TEMPLATE_PACK == 'uni_form' else 'btn'


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
    field_classes = 'reset resetButton' if TEMPLATE_PACK == 'uni_form' else 'btn btn-inverse'


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
        self.legend = legend
        self.css_class = kwargs.pop('css_class', '')
        self.css_id = kwargs.pop('css_id', None)
        # Overrides class variable with an instance level variable
        self.template = kwargs.pop('template', self.template)
        self.flat_attrs = flatatt(kwargs)

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):
        fields = ''
        for field in self.fields:
            fields += render_field(field, form, form_style, context,
                                   template_pack=template_pack)

        legend = ''
        if self.legend:
            legend = u'%s' % Template(text_type(self.legend)).render(context)
        return render_to_string(self.template, Context({'fieldset': self, 'legend': legend, 'fields': fields, 'form_style': form_style}))


class MultiField(LayoutObject):
    """ MultiField container. Renders to a MultiField <div> """
    template = "uni_form/layout/multifield.html"
    field_template = "uni_form/multifield.html"

    def __init__(self, label, *fields, **kwargs):
        self.fields = list(fields)
        self.label_html = label
        self.label_class = kwargs.pop('label_class', u'blockLabel')
        self.css_class = kwargs.pop('css_class', u'ctrlHolder')
        self.css_id = kwargs.pop('css_id', None)
        self.template = kwargs.pop('template', self.template)
        self.field_template = kwargs.pop('field_template', self.field_template)
        self.flat_attrs = flatatt(kwargs)

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):
        # If a field within MultiField contains errors
        if context['form_show_errors']:
            for field in map(lambda pointer: pointer[1], self.get_field_names()):
                if field in form.errors:
                    self.css_class += " error"

        fields_output = u''
        for field in self.fields:
            fields_output += render_field(
                field, form, form_style, context,
                self.field_template, self.label_class, layout_object=self,
                template_pack=template_pack
            )

        context.update({'multifield': self, 'fields_output': fields_output})
        return render_to_string(self.template, context)


class Div(LayoutObject):
    """
    Layout object. It wraps fields in a <div>

    You can set `css_id` for a DOM id and `css_class` for a DOM class. Example::

        Div('form_field_1', 'form_field_2', css_id='div-example', css_class='divs')
    """
    template = "uni_form/layout/div.html"

    def __init__(self, *fields, **kwargs):
        self.fields = list(fields)

        if hasattr(self, 'css_class') and 'css_class' in kwargs:
            self.css_class += ' %s' % kwargs.pop('css_class')
        if not hasattr(self, 'css_class'):
            self.css_class = kwargs.pop('css_class', None)

        self.css_id = kwargs.pop('css_id', '')
        self.template = kwargs.pop('template', self.template)
        self.flat_attrs = flatatt(kwargs)

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):
        fields = ''
        for field in self.fields:
            fields += render_field(field, form, form_style, context, template_pack=template_pack)

        return render_to_string(self.template, Context({'div': self, 'fields': fields}))


class Row(Div):
    """
    Layout object. It wraps fields in a div whose default class is "formRow". Example::

        Row('form_field_1', 'form_field_2', 'form_field_3')
    """
    css_class = 'formRow' if TEMPLATE_PACK == 'uni_form' else 'row'


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

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):
        return Template(text_type(self.html)).render(context)


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

        if 'css_class' in kwargs:
            if 'class' in self.attrs:
                self.attrs['class'] += " %s" % kwargs.pop('css_class')
            else:
                self.attrs['class'] = kwargs.pop('css_class')

        self.wrapper_class = kwargs.pop('wrapper_class', None)
        self.template = kwargs.pop('template', self.template)

        # We use kwargs as HTML attributes, turning data_id='test' into data-id='test'
        self.attrs.update(dict([(k.replace('_', '-'), conditional_escape(v)) for k, v in kwargs.items()]))

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):
        if hasattr(self, 'wrapper_class'):
            context['wrapper_class'] = self.wrapper_class

        html = ''
        for field in self.fields:
            html += render_field(field, form, form_style, context, template=self.template, attrs=self.attrs, template_pack=template_pack)
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
