from dataclasses import dataclass
from typing import List

from django.template import Template
from django.template.loader import render_to_string
from django.utils.html import conditional_escape
from django.utils.safestring import SafeString
from django.utils.text import slugify

from crispy_forms.utils import TEMPLATE_PACK, flatatt, render_field


@dataclass
class Pointer:
    positions: List[int]
    name: str


class TemplateNameMixin:
    def get_template_name(self, template_pack):
        if "%s" in self.template:
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
        if "fields" in self.__dict__ and hasattr(self.fields, name):
            return getattr(self.fields, name)
        else:
            return object.__getattribute__(self, name)

    def get_field_names(self, index=None):
        """
        Returns a list of Pointers. First parameter is the location of the
        field, second one the name of the field. Example::

            [
                Pointer([0,1,2], 'field_name1'),
                Pointer([0,3], 'field_name2'),
            ]
        """
        return self.get_layout_objects(str, index=None, greedy=True)

    def get_layout_objects(self, *LayoutClasses, index=None, max_level=0, greedy=False):
        """
        Returns a list of Pointers pointing to layout objects of any type matching
        `LayoutClasses`::

            [
                Pointer([0,1,2], 'div']),
                Pointer([0,3], 'field_name'),
            ]

        :param max_level: An integer that indicates max level depth to reach when
        traversing a layout.
        :param greedy: Boolean that indicates whether to be greedy. If set, max_level
        is skipped.
        """
        pointers = []

        if index is not None and not isinstance(index, list):
            index = [index]
        elif index is None:
            index = []

        str_class = len(LayoutClasses) == 1 and LayoutClasses[0] == str
        for i, layout_object in enumerate(self.fields):
            if isinstance(layout_object, LayoutClasses):
                if str_class:
                    pointers.append(Pointer(index + [i], layout_object))
                else:
                    pointers.append(Pointer(index + [i], layout_object.__class__.__name__.lower()))

            # If it's a layout object and we haven't reached the max depth limit or greedy
            # we recursive call
            if hasattr(layout_object, "get_field_names") and (len(index) < max_level or greedy):
                new_kwargs = {"index": index + [i], "max_level": max_level, "greedy": greedy}
                pointers = pointers + layout_object.get_layout_objects(*LayoutClasses, **new_kwargs)

        return pointers

    def get_rendered_fields(self, form, context, template_pack=TEMPLATE_PACK, **kwargs):
        return SafeString(
            "".join(render_field(field, form, context, template_pack=template_pack, **kwargs) for field in self.fields)
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

    def render(self, form, context, template_pack=TEMPLATE_PACK, **kwargs):
        return self.get_rendered_fields(form, context, template_pack, **kwargs)


class ButtonHolder(LayoutObject):
    """
    Layout object. It wraps fields in a <div class="buttonHolder">

    This is where you should put Layout objects that render to form buttons

    Attributes
    ----------
    template: str
        The default template which this Layout Object will be rendered
        with.

    Parameters
    ----------
    *fields : HTML or BaseInput
        The layout objects to render within the ``ButtonHolder``. It should
        only hold `HTML` and `BaseInput` inherited objects.
    css_id : str, optional
        A custom DOM id for the layout object. If not provided the name
        argument is slugified and turned into the id for the submit button.
        By default None.
    css_class : str, optional
        Additional CSS classes to be applied to the ``<input>``. By default
        None.
    template : str, optional
        Overrides the default template, if provided. By default None.

    Examples
    --------

    An example using ``ButtonHolder`` in your layout::

        ButtonHolder(
            HTML(<span style="display: hidden;">Information Saved</span>),
            Submit('Save', 'Save')
        )
    """

    template = "%s/layout/buttonholder.html"

    def __init__(self, *fields, css_id=None, css_class=None, template=None):
        self.fields = list(fields)
        self.css_id = css_id
        self.css_class = css_class
        self.template = template or self.template

    def render(self, form, context, template_pack=TEMPLATE_PACK, **kwargs):
        html = self.get_rendered_fields(form, context, template_pack, **kwargs)

        template = self.get_template_name(template_pack)
        context.update({"buttonholder": self, "fields_output": html})

        return render_to_string(template, context.flatten())


class BaseInput(TemplateNameMixin):
    """
    A base class to reduce the amount of code in the Input classes.

    Attributes
    ----------
    template: str
        The default template which this Layout Object will be rendered
        with.
    field_classes: str
        CSS classes to be applied to the ``<input>``.

    Parameters
    ----------
    name : str
        The name attribute of the button.
    value : str
        The value attribute of the button.
    css_id : str, optional
        A custom DOM id for the layout object. If not provided the name
        argument is slugified and turned into the id for the submit button.
        By default None.
    css_class : str, optional
        Additional CSS classes to be applied to the ``<input>``. By default
        None.
    template : str, optional
        Overrides the default template, if provided. By default None.
    **kwargs : dict, optional
        Additional attributes are passed to `flatatt` and converted into
        key="value", pairs. These attributes are added to the ``<input>``.
    """

    template = "%s/layout/baseinput.html"
    field_classes = ""

    def __init__(self, name, value, *, css_id=None, css_class=None, template=None, **kwargs):
        self.name = name
        self.value = value
        if css_id:
            self.id = css_id
        else:
            slug = slugify(self.name)
            self.id = f"{self.input_type}-id-{slug}"
        self.attrs = {}

        if css_class:
            self.field_classes += f" {css_class}"

        self.template = template or self.template
        self.flat_attrs = flatatt(kwargs)

    def render(self, form, context, template_pack=TEMPLATE_PACK, **kwargs):
        """
        Renders an `<input />` if container is used as a Layout object.
        Input button value can be a variable in context.
        """
        self.value = Template(str(self.value)).render(context)
        template = self.get_template_name(template_pack)
        context.update({"input": self})

        return render_to_string(template, context.flatten())


class Submit(BaseInput):
    """
    Used to create a Submit button descriptor for the {% crispy %} template tag.

    Attributes
    ----------
    template: str
        The default template which this Layout Object will be rendered
        with.
    field_classes: str
        CSS classes to be applied to the ``<input>``.
    input_type: str
        The ``type`` attribute of the ``<input>``.

    Parameters
    ----------
    name : str
        The name attribute of the button.
    value : str
        The value attribute of the button.
    css_id : str, optional
        A custom DOM id for the layout object. If not provided the name
        argument is slugified and turned into the id for the submit button.
        By default None.
    css_class : str, optional
        Additional CSS classes to be applied to the ``<input>``. By default
        None.
    template : str, optional
        Overrides the default template, if provided. By default None.
    **kwargs : dict, optional
        Additional attributes are passed to `flatatt` and converted into
        key="value", pairs. These attributes are added to the ``<input>``.

    Examples
    --------
    Note: ``form`` arg to ``render()`` is not required for ``BaseInput``
    inherited objects.

    >>> submit = Submit('Search the Site', 'search this site')
    >>> submit.render("", "", Context())
    '<input type="submit" name="search-the-site" value="search this site" '
    'class="btn btn-primary" id="submit-id-search-the-site"/>'

    >>> submit = Submit('Search the Site', 'search this site', css_id="custom-id",
                         css_class="custom class", my_attr=True, data="my-data")
    >>> submit.render("", "", Context())
    '<input type="submit" name="search-the-site" value="search this site" '
    'class="btn btn-primary custom class" id="custom-id" data="my-data" my-attr/>'

    Usually you will not call the render method on the object directly. Instead
    add it to your ``Layout`` manually or use the `add_input` method::

        class ExampleForm(forms.Form):
        [...]
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.add_input(Submit('submit', 'Submit'))
    """

    input_type = "submit"
    field_classes = "btn btn-primary"


class Button(BaseInput):
    """
    Used to create a button descriptor for the {% crispy %} template tag.

    Attributes
    ----------
    template: str
        The default template which this Layout Object will be rendered
        with.
    field_classes: str
        CSS classes to be applied to the ``<input>``.
    input_type: str
        The ``type`` attribute of the ``<input>``.

    Parameters
    ----------
    name : str
        The name attribute of the button.
    value : str
        The value attribute of the button.
    css_id : str, optional
        A custom DOM id for the layout object. If not provided the name
        argument is slugified and turned into the id for the submit button.
        By default None.
    css_class : str, optional
        Additional CSS classes to be applied to the ``<input>``. By default
        None.
    template : str, optional
        Overrides the default template, if provided. By default None.
    **kwargs : dict, optional
        Additional attributes are passed to `flatatt` and converted into
        key="value", pairs. These attributes are added to the ``<input>``.

    Examples
    --------
    Note: ``form`` arg to ``render()`` is not required for ``BaseInput``
    inherited objects.

    >>> button = Button('Button 1', 'Press Me!')
    >>> button.render("", "", Context())
    '<input type="button" name="button-1" value="Press Me!" '
    'class="btn" id="button-id-button-1"/>'

    >>> button = Button('Button 1', 'Press Me!', css_id="custom-id",
                         css_class="custom class", my_attr=True, data="my-data")
    >>> button.render("", "", Context())
    '<input type="button" name="button-1" value="Press Me!" '
    'class="btn custom class" id="custom-id" data="my-data" my-attr/>'

    Usually you will not call the render method on the object directly. Instead
    add it to your ``Layout`` manually or use the `add_input` method::

        class ExampleForm(forms.Form):
        [...]
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.add_input(Button('Button 1', 'Press Me!'))
    """

    input_type = "button"
    field_classes = "btn"


class Hidden(BaseInput):
    """
    Used to create a Hidden input descriptor for the {% crispy %} template tag.

    Attributes
    ----------
    template: str
        The default template which this Layout Object will be rendered
        with.
    field_classes: str
        CSS classes to be applied to the ``<input>``.
    input_type: str
        The ``type`` attribute of the ``<input>``.

    Parameters
    ----------
    name : str
        The name attribute of the button.
    value : str
        The value attribute of the button.
    css_id : str, optional
        A custom DOM id for the layout object. If not provided the name
        argument is slugified and turned into the id for the submit button.
        By default None.
    css_class : str, optional
        Additional CSS classes to be applied to the ``<input>``. By default
        None.
    template : str, optional
        Overrides the default template, if provided. By default None.
    **kwargs : dict, optional
        Additional attributes are passed to `flatatt` and converted into
        key="value", pairs. These attributes are added to the ``<input>``.

    Examples
    --------
    Note: ``form`` arg to ``render()`` is not required for ``BaseInput``
    inherited objects.

    >>> hidden = Hidden("hidden", "hide-me")
    >>> hidden.render("", "", Context())
    '<input type="hidden" name="hidden" value="hide-me"/>'

    Usually you will not call the render method on the object directly. Instead
    add it to your ``Layout`` manually or use the `add_input` method::

        class ExampleForm(forms.Form):
        [...]
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.add_input(Hidden("hidden", "hide-me"))
    """

    input_type = "hidden"
    field_classes = "hidden"


class Reset(BaseInput):
    """
    Used to create a reset button descriptor for the {% crispy %} template tag.

    Attributes
    ----------
    template: str
        The default template which this Layout Object will be rendered
        with.
    field_classes: str
        CSS classes to be applied to the ``<input>``.
    input_type: str
        The ``type`` attribute of the ``<input>``.

    Parameters
    ----------
    name : str
        The name attribute of the button.
    value : str
        The value attribute of the button.
    css_id : str, optional
        A custom DOM id for the layout object. If not provided the name
        argument is slugified and turned into the id for the submit button.
        By default None.
    css_class : str, optional
        Additional CSS classes to be applied to the ``<input>``. By default
        None.
    template : str, optional
        Overrides the default template, if provided. By default None.
    **kwargs : dict, optional
        Additional attributes are passed to `flatatt` and converted into
        key="value", pairs. These attributes are added to the ``<input>``.

    Examples
    --------
    Note: ``form`` arg to ``render()`` is not required for ``BaseInput``
    inherited objects.

    >>> reset = Reset('Reset This Form', 'Revert Me!')
    >>> reset.render("", "", Context())
    '<input type="reset" name="reset-this-form" value="Revert Me!" '
    'class="btn btn-inverse" id="reset-id-reset-this-form"/>'

    >>> reset = Reset('Reset This Form', 'Revert Me!', css_id="custom-id",
                         css_class="custom class", my_attr=True, data="my-data")
    >>> reset.render("", "", Context())
    '<input type="reset" name="reset-this-form" value="Revert Me!" '
    'class="btn btn-inverse custom class" id="custom-id" data="my-data" my-attr/>'

    Usually you will not call the render method on the object directly. Instead
    add it to your ``Layout`` manually manually or use the `add_input` method::

        class ExampleForm(forms.Form):
        [...]
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.add_input(Reset('Reset This Form', 'Revert Me!'))
    """

    input_type = "reset"
    field_classes = "btn btn-inverse"


class Fieldset(LayoutObject):
    """
    A layout object which wraps fields in a ``<fieldset>``

    Parameters
    ----------
    legend : str
        The content of the fieldset's ``<legend>``. This text is context
        aware, to bring this to life see the examples section.
    *fields : str | LayoutObject | HTML
        Any number of fields as positional arguments to be rendered within
        the ``<fieldset>``
    css_class : str, optional
        Additional CSS classes to be applied to the ``<input>``. By default
        None.
    css_id : str, optional
        A custom DOM id for the layout object. If not provided the name
        argument is slugified and turned into the id for the submit button.
        By default None.
    template : str, optional
        Overrides the default template, if provided. By default None.
    **kwargs : dict, optional
        Additional attributes are passed to ``flatatt`` and converted into
        key="value", pairs. These attributes are added to the ``<fieldset>``.

    Examples
    --------

    The Fieldset Layout object is added to your ``Layout`` for example::

        Fieldset("Text for the legend",
            "form_field_1",
            "form_field_2",
            css_id="my-fieldset-id",
            css_class="my-fieldset-class",
            data="my-data"
        )

    The above layout will be rendered as::

        '''
        <fieldset id="fieldset-id" class="my-fieldset-class" data="my-data">
           <legend>Text for the legend</legend>
           # form fields render here
        </fieldset>
        '''

    The first parameter is the text for the fieldset legend. This text is context aware,
    so you can do things like::

        Fieldset("Data for {{ user.username }}",
            'form_field_1',
            'form_field_2'
        )
    """

    template = "%s/layout/fieldset.html"

    def __init__(self, legend, *fields, css_class=None, css_id=None, template=None, **kwargs):
        self.fields = list(fields)
        self.legend = legend
        self.css_class = css_class
        self.css_id = css_id
        self.template = template or self.template
        self.flat_attrs = flatatt(kwargs)

    def render(self, form, context, template_pack=TEMPLATE_PACK, **kwargs):
        fields = self.get_rendered_fields(form, context, template_pack, **kwargs)

        if self.legend:
            legend = Template(str(self.legend)).render(context)
        else:
            legend = SafeString("")

        template = self.get_template_name(template_pack)
        return render_to_string(template, {"fieldset": self, "legend": legend, "fields": fields})


class MultiField(LayoutObject):
    """
    MultiField container for Bootstrap3. Renders to a MultiField <div>.

    Attributes
    ----------
    template: str
        The default template which this Layout Object will be rendered
        with.
    field_template: str
        The template which fields will be rendered with.

    Parameters
    ----------
    label: str
        The label for the multifield.
    *fields: str
        The fields to be rendered within the multifield.
    label_class: str, optional
        CSS classes to be added to the multifield label. By default None.
    help_text: str, optional
        Help text will be available in the context of the multifield template.
        This is unused in the bootstrap3 template provided. By default None.
    css_class : str, optional
        Additional CSS classes to be applied to the ``<input>``. By default
        None.
    css_id : str, optional
        A DOM id for the layout object which will be added to the wrapping
        ``<div>`` if provided. By default None.
    template : str, optional
        Overrides the default template, if provided. By default None.
    field_template : str, optional
        Overrides the default template, if provided. By default None.
    **kwargs : dict, optional
        Additional attributes are passed to ``flatatt`` and converted into
        key="value", pairs. These attributes are added to the wrapping
        ``<div>``.

    """

    template = "%s/layout/multifield.html"
    field_template = "%s/multifield.html"

    def __init__(
        self,
        label,
        *fields,
        label_class=None,
        help_text=None,
        css_class=None,
        css_id=None,
        template=None,
        field_template=None,
        **kwargs,
    ):
        self.fields = list(fields)
        self.label_html = label
        self.label_class = label_class or "blockLabel"
        self.css_class = css_class or "ctrlHolder"
        self.css_id = css_id
        self.help_text = help_text
        self.template = template or self.template
        self.field_template = field_template or self.field_template
        self.flat_attrs = flatatt(kwargs)

    def render(self, form, context, template_pack=TEMPLATE_PACK, **kwargs):
        # If a field within MultiField contains errors
        if context["form_show_errors"]:
            for field in (pointer.name for pointer in self.get_field_names()):
                if field in form.errors:
                    self.css_class += " error"

        field_template = self.field_template % template_pack
        fields_output = self.get_rendered_fields(
            form,
            context,
            template_pack,
            template=field_template,
            labelclass=self.label_class,
            layout_object=self,
            **kwargs,
        )

        template = self.get_template_name(template_pack)
        context.update({"multifield": self, "fields_output": fields_output})

        return render_to_string(template, context.flatten())


class Div(LayoutObject):
    """
    Layout object. It wraps fields in a ``<div>``.

    Attributes
    ----------
    template : str
        The default template which this Layout Object will be rendered
        with.
    css_class : str, optional
        CSS classes to be applied to the ``<div>``. By default None.

    Parameters
    ----------
    *fields : str, LayoutObject
        Any number of fields as positional arguments to be rendered within
        the ``<div>``.
    css_id : str, optional
        A DOM id for the layout object which will be added to the ``<div>`` if
        provided. By default None.
    css_class : str, optional
        Additional CSS classes to be applied in addition to those declared by
        the class itself. By default None.
    template : str, optional
        Overrides the default template, if provided. By default None.
    **kwargs : dict, optional
        Additional attributes are passed to ``flatatt`` and converted into
        key="value", pairs. These attributes are added to the ``<div>``.

    Examples
    --------

    In your ``Layout`` you can::

        Div(
            'form_field_1',
            'form_field_2',
            css_id='div-example',
            css_class='divs',
        )

    It is also possible to nest Layout Objects within a Div::

        Div(
            Div(
                Field('form_field', css_class='field-class'),
                css_class='div-class',
            ),
            Div('form_field_2', css_class='div-class'),
        )
    """

    template = "%s/layout/div.html"
    css_class = None

    def __init__(self, *fields, css_id=None, css_class=None, template=None, **kwargs):
        self.fields = list(fields)

        if self.css_class and css_class:
            self.css_class += f" {css_class}"
        elif css_class:
            self.css_class = css_class

        self.css_id = css_id
        self.template = template or self.template
        self.flat_attrs = flatatt(kwargs)

    def render(self, form, context, template_pack=TEMPLATE_PACK, **kwargs):
        fields = self.get_rendered_fields(form, context, template_pack, **kwargs)

        template = self.get_template_name(template_pack)
        return render_to_string(template, {"div": self, "fields": fields})


class Row(Div):
    """
    Layout object. It wraps fields in a ``<div>`` and the template adds the
    appropriate class to render the contents in a row. e.g. ``form-row`` when
    using the Bootstrap4 template pack.

    Attributes
    ----------
    template : str
        The default template which this Layout Object will be rendered
        with.
    css_class : str, optional
        CSS classes to be applied to the ``<div>``. By default None.

    Parameters
    ----------
    *fields : str, LayoutObject
        Any number of fields as positional arguments to be rendered within
        the ``<div>``.
    css_id : str, optional
        A DOM id for the layout object which will be added to the ``<div>`` if
        provided. By default None.
    css_class : str, optional
        Additional CSS classes to be applied in addition to those declared by
        the class itself. By default None.
    template : str, optional
        Overrides the default template, if provided. By default None.
    **kwargs : dict, optional
        Additional attributes are passed to ``flatatt`` and converted into
        key="value", pairs. These attributes are added to the ``<div>``.

    Examples
    --------

    In your ``Layout`` you can::

        Row('form_field_1', 'form_field_2', css_id='row-example')

    It is also possible to nest Layout Objects within a Row::

        Row(
            Div(
                Field('form_field', css_class='field-class'),
                css_class='div-class',
            ),
            Div('form_field_2', css_class='div-class'),
        )
    """

    template = "%s/layout/row.html"


class Column(Div):
    """
    Layout object. It wraps fields in a ``<div>`` and the template adds the
    appropriate class to render the contents in a column. e.g. ``col-md`` when
    using the Bootstrap4 template pack.

    Attributes
    ----------
    template : str
        The default template which this Layout Object will be rendered
        with.
    css_class : str, optional
        CSS classes to be applied to the ``<div>``. By default None.

    Parameters
    ----------
    *fields : str, LayoutObject
        Any number of fields as positional arguments to be rendered within
        the ``<div>``.
    css_id : str, optional
        A DOM id for the layout object which will be added to the ``<div>`` if
        provided. By default None.
    css_class : str, optional
        Additional CSS classes to be applied in addition to those declared by
        the class itself. If using the Bootstrap4 template pack the default
        ``col-md`` is removed if this string contins another ``col-`` class.
        By default None.
    template : str, optional
        Overrides the default template, if provided. By default None.
    **kwargs : dict, optional
        Additional attributes are passed to ``flatatt`` and converted into
        key="value", pairs. These attributes are added to the ``<div>``.

    Examples
    --------

    In your ``Layout`` you can::

        Column('form_field_1', 'form_field_2', css_id='col-example')

    It is also possible to nest Layout Objects within a Row::

        Div(
            Column(
                Field('form_field', css_class='field-class'),
                css_class='col-sm,
            ),
            Column('form_field_2', css_class='col-sm'),
        )
    """

    template = "%s/layout/column.html"


class HTML:
    """
    Layout object. It can contain pure HTML and it has access to the whole
    context of the page where the form is being rendered.

    Examples::

        HTML("{% if saved %}Data saved{% endif %}")
        HTML('<input type="hidden" name="{{ step_field }}" value="{{ step0 }}" />')
    """

    def __init__(self, html):
        self.html = html

    def render(self, form, context, template_pack=TEMPLATE_PACK, **kwargs):
        return Template(str(self.html)).render(context)


class Field(LayoutObject):
    """
    A Layout object, usually containing one field name, where you can add
    attributes to it easily.

    Attributes
    ----------
    template : str
        The default template which this Layout Object will be rendered
        with.
    attrs : dict
        Attributes to be applied to the field. These are converted into html
        attributes. e.g. ``data_id: 'test'`` in the attrs dict will become
        ``data-id='test'`` on the field's ``<input>``.

    Parameters
    ----------
    *fields : str
        Usually a single field, but can be any number of fields, to be rendered
        with the same attributes applied.
    css_class : str, optional
        CSS classes to be applied to the field. These are added to any classes
        included in the ``attrs`` dict. By default ``None``.
    wrapper_class: str, optional
        CSS classes to be used when rendering the Field. This class is usually
        applied to the ``<div>`` which wraps the Field's ``<label>`` and
        ``<input>`` tags. By default ``None``.
    template : str, optional
        Overrides the default template, if provided. By default ``None``.
    **kwargs : dict, optional
        Additional attributes are converted into key="value", pairs. These
        attributes are added to the ``<div>``.

    Examples
    --------

    Example::

        Field('field_name', style="color: #333;", css_class="whatever", id="field_name")
    """

    template = "%s/field.html"
    attrs = {}

    def __init__(self, *fields, css_class=None, wrapper_class=None, template=None, **kwargs):
        self.fields = list(fields)
        # Make sure shared state is not edited.
        self.attrs = self.attrs.copy()

        if css_class:
            if "class" in self.attrs:
                self.attrs["class"] += f" {css_class}"
            else:
                self.attrs["class"] = css_class

        self.wrapper_class = wrapper_class
        self.template = template or self.template

        # We use kwargs as HTML attributes, turning data_id='test' into data-id='test'
        self.attrs.update({k.replace("_", "-"): conditional_escape(v) for k, v in kwargs.items()})

    def render(self, form, context, template_pack=TEMPLATE_PACK, extra_context=None, **kwargs):
        if extra_context is None:
            extra_context = {}
        if self.wrapper_class:
            extra_context["wrapper_class"] = self.wrapper_class

        template = self.get_template_name(template_pack)

        return self.get_rendered_fields(
            form,
            context,
            template_pack,
            template=template,
            attrs=self.attrs,
            extra_context=extra_context,
            **kwargs,
        )


class MultiWidgetField(Field):
    """
    Layout object. For fields with :class:`~django.forms.MultiWidget` as
    ``widget``, you can pass additional attributes to each widget.

    Attributes
    ----------
    template : str
        The default template which this Layout Object will be rendered
        with.

    Parameters
    ----------
    *fields : str
        Usually a single field, but can be any number of fields, to be rendered
        with the same attributes applied.
    attrs : str, optional
        Additional attrs to be added to each widget. These are added to any
        classes included in the ``attrs`` dict. By default ``None``.
    wrapper_class: str, optional
        CSS classes to be used when rendering the Field. This class is usually
        applied to the ``<div>`` which wraps the Field's ``<label>`` and
        ``<input>`` tags. By default ``None``.
    template : str, optional
        Overrides the default template, if provided. By default ``None``.

    Examples
    --------

    Example::

        MultiWidgetField(
            'multiwidget_field_name',
            attrs=(
                {'style': 'width: 30px;'},
                {'class': 'second_widget_class'}
            ),
        )
    """

    def __init__(self, *fields, attrs=None, template=None, wrapper_class=None):
        self.fields = list(fields)
        self.attrs = attrs or {}
        self.template = template or self.template
        self.wrapper_class = wrapper_class
