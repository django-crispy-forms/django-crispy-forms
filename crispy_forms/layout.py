import itertools
import re

from django.conf import settings
from django.template import Context, Template
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.utils.html import conditional_escape

from utils import render_field, flatatt
from exceptions import DynamicError

TEMPLATE_PACK = getattr(settings, 'CRISPY_TEMPLATE_PACK', 'bootstrap')


class LayoutObject(object):
    def __getitem__(self, slice):
        return self.fields[slice]

    def __setitem__(self, slice, value):
        self.fields[slice] = value

    def __getattr__(self, name):
        """
        This allows us to access self.fields list methods like append or insert, without
        having to declare them one by one
        """
        if hasattr(self.fields, name):
            return getattr(self.fields, name)
        else:
            return object.__getattribute__(self, name)

    def get_field_names(self, index=None):
        """
        Returns a list of lists, those lists are pointers to field names. First parameter
        is the location of the field, second one the name of the field. Example::

            [
               [[0,1,2], 'field_name1'],
               [[0,3], 'field_name2']
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
                        field_names = field_names + layout_object.get_field_names(index + [i])
                # If it's a string, then it's a basic case
                else:
                    field_names.append([index + [i], layout_object])

            return field_names

        # Base case: It only contains field_names
        else:
            fields_to_return = []
            for i, field_name in enumerate(self.fields):
                fields_to_return.append([index + [i], field_name])

            # If all the pointers to fields gathered are of length 2, we are done
            if all(len(pointer) == 2 for pointer in fields_to_return):
                return fields_to_return
            else:
                return list(itertools.chain.from_iterable(fields_to_return))

    def get_layout_objects(self, *LayoutClasses, **kwargs):
        """
        Returns a list of lists pointing to layout objects of type `LayoutClass`::

            [
               [[0,1,2]],
               [[0,3]]
            ]

        It traverses the layout reaching `max_level` depth
        """
        index = kwargs.pop('index', None)
        max_level = kwargs.pop('max_level', 0)

        pointers = []

        if index is not None and not isinstance(index, list):
            index = [index]
        elif index is None:
            index = []

        for i, layout_object in enumerate(self.fields):
            if isinstance(layout_object, LayoutClasses):
                pointers.append(index + [i])

            # If it's a layout object and we haven't reached the max depth limit
            # we recursive call
            if hasattr(layout_object, 'get_field_names') and len(index) < max_level:
                pointers = pointers + layout_object.get_layout_objects(
                    LayoutClasses, index=index + [i], max_level=max_level
                )

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
            for pointer in self.slice:
                # A list of integer pointers [0, 0]
                if len(pointer) != 2 or not isinstance(pointer[1], basestring):

                    layout_object = self.layout.fields[pointer[0]]
                    # Iterate until the last one
                    for i in pointer[1:-1]:
                        layout_object = layout_object.fields[i]

                    try:
                        self.layout.fields[pointer[-1]] = LayoutClass(self.layout.fields[pointer[-1]], **kwargs)
                    except IndexError:
                        # We could avoid this exception, recalculating pointers.
                        # However this case is most of the time an undesired behavior
                        raise DynamicError("Trying to wrap a field within an already wrapped field, \
                            recheck your filter or layout")

                # A list of field_name pointers [[0, 0], 'field_name']
                else:
                    pos = pointer[0]
                    layout_object = self.layout.fields[pos[0]]
                    for i in pointer[0][1:-1]:
                        layout_object = layout_object.fields[i]

                    # If layout object has a fields attribute
                    if hasattr(layout_object, 'fields'):
                        layout_object.fields[pos[-1]] = LayoutClass(layout_object.fields[pos[-1]], **kwargs)
                    else:
                        # Otherwise it's a basestring (a field name)
                        self.layout.fields[pos[0]] = LayoutClass(layout_object, **kwargs)


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
    template = "%s/layout/baseinput.html" % TEMPLATE_PACK

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
        self.legend = legend
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
            legend = u'%s' % Template(unicode(self.legend)).render(context)
        return render_to_string(self.template, Context({'fieldset': self, 'legend': legend, 'fields': fields, 'form_style': form_style}))


class MultiField(LayoutObject):
    """ multiField container. Renders to a multiField <div> """
    template = "uni_form/layout/multifield.html"

    def __init__(self, label, *fields, **kwargs):
        #TODO: Decide on how to support css classes for both container divs
        self.fields = list(fields)
        self.label_html = label
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
    css_class = 'formRow' if TEMPLATE_PACK == 'uni_form' else 'row'


class Tab(Div):
    """
    Tab object. It wraps fields in a div whose default class is "tab-pane" and
    take a name as first argument. Example::
        Tab('tab_name', 'form_field_1', 'form_field_2', 'form_field_3')
    """
    css_class = 'tab-pane'
    link_template = 'bootstrap/layout/tab-link.html'

    def __init__(self, name, *fields, **kwargs):
	self.name = name
	super(Tab, self).__init__(*fields, **kwargs)
	# id is necessary for the TabHolder links
	if not self.css_id:
	    self.css_id = slugify(self.name)
	self.active = False

    def __contains__(self, field):
	return field in self.fields

    def render_link(self):
	"""
	Render the link for the tab-pane. It must be call after render so css_class is updated
	with active if needed.
	"""
	return render_to_string(self.link_template, Context({'link': self}))

    def render(self, form, form_style, context):
	if self.active:
	    self.css_class += ' active'
	return super(Tab, self).render(form, form_style, context)


class TabHolder(Div):
    """
    TabHolder object. It wraps Tab objects in a container. 
    *REQUIRES bootstrap-tab.js*
	Example::  TabHolder(Tab('form_field_1', 'form_field_2'), Tab('form_field_3'))
    """
    template = 'bootstrap/layout/tab.html'
    css_class = 'nav nav-tabs'

    def first_tab_with_errors(self, errors):
	"""
	Return the first tab with errors in fields or the first tab if there are no errors.
	"""
	for tab in self.fields:
	    errors_here = bool(filter(lambda err: err in tab, errors))
	    if errors_here:
		return tab
	return self.fields[0]

    def render(self, form, form_style, context):
	flds = self.fields
	links, content = '', ''
	self.first_tab_with_errors(form.errors.keys()).active = True
	for tab in self.fields:
	    content += render_field(tab, form, form_style, context)
	    links += tab.render_link()
	return render_to_string(self.template, 
	    Context({'tabs': self, 'links': links, 'content': content}))


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

    def render(self, form, form_style, context):
        return Template(unicode(self.html)).render(context)


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
