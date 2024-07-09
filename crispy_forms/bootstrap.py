from random import randint

from django.template import Template
from django.template.loader import render_to_string
from django.utils.safestring import SafeString
from django.utils.text import slugify

from .layout import Div, Field, LayoutObject, TemplateNameMixin
from .utils import TEMPLATE_PACK, flatatt, render_field


class PrependedAppendedText(Field):
    """
    Layout object for rendering a field with prepended and appended text.

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
    field : str
        The name of the field to be rendered.
    prepended_text : str, optional
        The prepended text, can be HTML like, by default None
    appended_text : str, optional
        The appended text, can be HTML like, by default None
    input_size : str, optional
        For Bootstrap4+ additional classes to customise the input-group size
        e.g. ``input-group-sm``. By default None
    active : bool
        For Bootstrap3, a boolean to render the text active. By default
        ``False``.
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

         PrependedAppendedText('amount', '$', '.00')
    """

    template = "%s/layout/prepended_appended_text.html"

    def __init__(
        self,
        field,
        prepended_text=None,
        appended_text=None,
        input_size=None,
        *,
        active=False,
        css_class=None,
        wrapper_class=None,
        template=None,
        **kwargs,
    ):
        self.field = field
        self.appended_text = appended_text
        self.prepended_text = prepended_text
        self.active = active

        self.input_size = input_size

        if css_class:  # Bootstrap 3
            if "input-lg" in css_class:
                self.input_size = "input-lg"
            if "input-sm" in css_class:
                self.input_size = "input-sm"

        super().__init__(field, css_class=css_class, wrapper_class=wrapper_class, template=template, **kwargs)

    def render(self, form, context, template_pack=TEMPLATE_PACK, extra_context=None, **kwargs):
        extra_context = extra_context.copy() if extra_context is not None else {}
        extra_context.update(
            {
                "crispy_appended_text": self.appended_text,
                "crispy_prepended_text": self.prepended_text,
                "input_size": self.input_size,
                "active": getattr(self, "active", False),
                "wrapper_class": self.wrapper_class,
            }
        )
        template = self.get_template_name(template_pack)
        return render_field(
            self.field,
            form,
            context,
            template=template,
            attrs=self.attrs,
            template_pack=template_pack,
            extra_context=extra_context,
            **kwargs,
        )


class AppendedText(PrependedAppendedText):
    """
    Layout object for rendering a field with appended text.

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
    field : str
        The name of the field to be rendered.
    text : str
        The appended text, can be HTML like.
    input_size : str, optional
        For Bootstrap4+ additional classes to customise the input-group size
        e.g. ``input-group-sm``. By default None
    active : bool
        For Bootstrap3, a boolean to render the text active. By default
        ``False``.
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

         AppendedText('amount', '.00')
    """

    def __init__(
        self,
        field,
        text,
        *,
        input_size=None,
        active=False,
        css_class=None,
        wrapper_class=None,
        template=None,
        **kwargs,
    ):
        self.text = text
        super().__init__(
            field,
            appended_text=text,
            input_size=input_size,
            active=active,
            css_class=css_class,
            wrapper_class=wrapper_class,
            template=template,
            **kwargs,
        )


class PrependedText(PrependedAppendedText):
    """
    Layout object for rendering a field with prepended text.

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
    field : str
        The name of the field to be rendered.
    text : str
        The prepended text, can be HTML like.
    input_size : str, optional
        For Bootstrap4+ additional classes to customise the input-group size
        e.g. ``input-group-sm``. By default None
    active : bool
        For Bootstrap3, a boolean to render the text active. By default
        ``False``.
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

         PrependedText('amount', '$')
    """

    def __init__(
        self,
        field,
        text,
        *,
        input_size=None,
        active=False,
        css_class=None,
        wrapper_class=None,
        template=None,
        **kwargs,
    ):
        self.text = text
        super().__init__(
            field,
            prepended_text=text,
            input_size=input_size,
            active=active,
            css_class=css_class,
            wrapper_class=wrapper_class,
            template=template,
            **kwargs,
        )


class FormActions(LayoutObject):
    """
    Bootstrap layout object. It wraps fields in a <div class="form-actions">

    Attributes
    ----------
    template: str
        The default template which this Layout Object will be rendered with.

    Parameters
    ----------

    *fields : HTML or BaseInput
        The layout objects to render within the ``ButtonHolder``. It should
        only hold `HTML` and `BaseInput` inherited objects.
    css_id : str, optional
        A custom DOM id for the layout object which will be added to the
        ``<div>`` if provided. By default None.
    css_class : str, optional
        Additional CSS classes to be applied to the ``<div>``. By default
        None.
    template : str, optional
        Overrides the default template, if provided. By default None.
    **kwargs : dict, optional
        Additional attributes are passed to ``flatatt`` and converted into
        key="value", pairs. These attributes are added to the ``<div>``.

    Examples
    --------

    An example using ``FormActions`` in your layout::

        FormActions(
            HTML(<span style="display: hidden;">Information Saved</span>),
            Submit('Save', 'Save', css_class='btn-primary')
        )
    """

    template = "%s/layout/formactions.html"

    def __init__(self, *fields, css_id=None, css_class=None, template=None, **kwargs):
        self.fields = list(fields)
        self.id = css_id
        self.css_class = css_class
        self.template = template or self.template
        self.flat_attrs = flatatt(kwargs)

    def render(self, form, context, template_pack=TEMPLATE_PACK, **kwargs):
        html = self.get_rendered_fields(form, context, template_pack, **kwargs)
        template = self.get_template_name(template_pack)
        context.update({"formactions": self, "fields_output": html})

        return render_to_string(template, context.flatten())


class InlineCheckboxes(Field):
    """
    Layout object for rendering checkboxes inline.

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

        InlineCheckboxes('field_name')
    """

    template = "%s/layout/checkboxselectmultiple_inline.html"

    def render(self, form, context, template_pack=TEMPLATE_PACK, **kwargs):
        return super().render(form, context, template_pack=template_pack, extra_context={"inline_class": "inline"})


class InlineRadios(Field):
    """
    Layout object for rendering radiobuttons inline.

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

        InlineRadios('field_name')
    """

    template = "%s/layout/radioselect_inline.html"

    def render(self, form, context, template_pack=TEMPLATE_PACK, **kwargs):
        return super().render(form, context, template_pack=template_pack, extra_context={"inline_class": "inline"})


class FieldWithButtons(Div):
    """
    A layout object for rendering a single field with any number of buttons.

    Attributes
    ----------
    template : str
        The default template which this Layout Object will be rendered
        with.
    css_class : str, optional
        CSS classes to be applied to the wrapping ``<div>``. By default None.

    Parameters
    ----------

    *fields : str or LayoutObject
        The first positional argument is the field. This can be either the
        name of the field as a string or an instance of `Field`. Following
        arguments will be rendered as buttons.
    input_size : str
        Additional CSS class to change the size of the input. e.g.
        "input-group-sm".
    css_id : str, optional
        A DOM id for the layout object which will be added to the wrapping
        ``<div>`` if provided. By default None.
    css_class : str, optional
        Additional CSS classes to be applied in addition to those declared by
        the class itself. By default None.
    template : str, optional
        Overrides the default template, if provided. By default None.
    **kwargs : dict, optional
        Additional attributes are passed to ``flatatt`` and converted into
        key="value", pairs. These attributes are added to the wrapping
        ``<div>``.

    Examples
    --------

    Example::

        FieldWithButtons(
            Field("password1", css_class="span4"),
            StrictButton("Go!", css_id="go-button"),
            input_size="input-group-sm",
        )
    """

    template = "%s/layout/field_with_buttons.html"
    field_template = "%s/field.html"

    def __init__(self, *fields, input_size=None, css_id=None, css_class=None, template=None, **kwargs):
        self.input_size = input_size
        super().__init__(*fields, css_id=css_id, css_class=css_class, template=template, **kwargs)

    def render(self, form, context, template_pack=TEMPLATE_PACK, extra_context=None, **kwargs):
        # We first render the buttons
        field_template = self.field_template % template_pack
        buttons = SafeString(
            "".join(
                render_field(
                    field,
                    form,
                    context,
                    field_template,
                    layout_object=self,
                    template_pack=template_pack,
                    **kwargs,
                )
                for field in self.fields[1:]
            )
        )

        extra_context = {"div": self, "buttons": buttons}
        template = self.get_template_name(template_pack)

        if isinstance(self.fields[0], Field):
            # FieldWithButtons(Field('field_name'), StrictButton("go"))
            # We render the field passing its name and attributes
            return render_field(
                self.fields[0][0],
                form,
                context,
                template,
                attrs=self.fields[0].attrs,
                template_pack=template_pack,
                extra_context=extra_context,
                **kwargs,
            )
        else:
            return render_field(self.fields[0], form, context, template, extra_context=extra_context, **kwargs)


class StrictButton(TemplateNameMixin):
    """
    Layout object for rendering an HTML button in a ``<button>`` tag.

    Attributes
    ----------
    template: str
        The default template which this Layout Object will be rendered
        with.
    field_classes : str
        The CSS classes to be applied to the button. By defult "btn".

    Parameters
    ----------
    content : str
        The content of the button. This content is context aware, to bring
        this to life see the examples section.
    css_id : str, optional
        A custom DOM id for the layout object which will be added to the
        ``<button>`` if provided. By default None.
    css_class : str, optional
        Additional CSS classes to be applied to the ``<button>``. By default
        None.
    template : str, optional
        Overrides the default template, if provided. By default None.
    **kwargs : dict, optional
        Additional attributes are passed to `flatatt` and converted into
        key="value", pairs. These attributes are added to the ``<button>``.

    Examples
    --------

    In your ``Layout``::

        StrictButton("button content", css_class="extra")

    The content of the button is context aware, so you can do things like::

        StrictButton("Button for {{ user.username }}")
    """

    template = "%s/layout/button.html"
    field_classes = "btn"

    def __init__(self, content, css_id=None, css_class=None, template=None, **kwargs):
        self.content = content
        self.template = template or self.template

        kwargs.setdefault("type", "button")

        # We turn css_id and css_class into id and class
        if css_id:
            kwargs["id"] = css_id

        kwargs["class"] = self.field_classes
        if css_class:
            kwargs["class"] += f" {css_class}"

        self.flat_attrs = flatatt(kwargs)

    def render(self, form, context, template_pack=TEMPLATE_PACK, **kwargs):
        self.content = Template(str(self.content)).render(context)
        template = self.get_template_name(template_pack)
        context.update({"button": self})

        return render_to_string(template, context.flatten())


class Container(Div):
    """
    Base class used for `Tab` and `AccordionGroup`, represents a basic
    container concept.

    Attributes
    ----------
    template : str
        The default template which this Layout Object will be rendered
        with.
    css_class : str, optional
        CSS classes to be applied to the ``<div>``. By default "".

    Parameters
    ----------
    name : str
        The name of the container.
    *fields : str, LayoutObject
        Any number of fields as positional arguments to be rendered within
        the container.
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
    """

    css_class = ""

    def __init__(self, name, *fields, css_id=None, css_class=None, template=None, active=None, **kwargs):
        super().__init__(*fields, css_id=css_id, css_class=css_class, template=template, **kwargs)
        self.name = name
        self._active_originally_included = active is not None
        self.active = active or False
        if not self.css_id:
            self.css_id = slugify(self.name, allow_unicode=True)

    def __contains__(self, field_name):
        """
        check if field_name is contained within tab.
        """
        return field_name in (pointer.name for pointer in self.get_field_names())


class ContainerHolder(Div):
    """
    Base class used for `TabHolder` and `Accordion`, groups containers.

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
        Any number of fields or layout objects as positional arguments to be
        rendered within the ``<div>``.
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
    """

    def first_container_with_errors(self, errors):
        """
        Returns the first container with errors, otherwise returns None.
        """
        for tab in self.fields:
            errors_here = any(error in tab for error in errors)
            if errors_here:
                return tab
        return None

    def open_target_group_for_form(self, form):
        """
        Makes sure that the first group that should be open is open.
        This is either the first group with errors or the first group
        in the container, unless that first group was originally set to
        active=False.
        """
        target = self.first_container_with_errors(form.errors.keys())
        if target is None:
            target = self.fields[0]
            if not getattr(target, "_active_originally_included", None):
                target.active = True
            return target

        target.active = True
        return target


class Tab(Container):
    """
    Tab object. It wraps fields in a div whose default class is "tab-pane" and
    takes a name as first argument.

    Attributes
    ----------
    template : str
        The default template which this Layout Object will be rendered
        with.
    css_class : str, optional
        CSS classes to be applied to the ``<div>``. By default "".

    Parameters
    ----------
    name : str
        The name of the container.
    *fields : str, LayoutObject
        Any number of fields as positional arguments to be rendered within
        the container.
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

    Example::

        Tab('tab_name', 'form_field_1', 'form_field_2', 'form_field_3')
    """

    css_class = "tab-pane"
    link_template = "%s/layout/tab-link.html"

    def render_link(self, template_pack=TEMPLATE_PACK, **kwargs):
        """
        Render the link for the tab-pane. It must be called after render so css_class is updated
        with active if needed.
        """
        link_template = self.link_template % template_pack
        return render_to_string(link_template, {"link": self})

    def render(self, form, context, template_pack=TEMPLATE_PACK, **kwargs):
        if self.active:
            if "active" not in self.css_class:
                self.css_class += " active"
        else:
            self.css_class = self.css_class.replace("active", "")
        return super().render(form, context, template_pack)


class TabHolder(ContainerHolder):
    """
    TabHolder object. It wraps Tab objects in a container.

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
        Any number of fields or layout objects as positional arguments to be
        rendered within the ``<div>``.
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
    Example::

        TabHolder(
            Tab('form_field_1', 'form_field_2'),
            Tab('form_field_3')
        )
    """

    template = "%s/layout/tab.html"

    def render(self, form, context, template_pack=TEMPLATE_PACK, **kwargs):
        for tab in self.fields:
            tab.active = False

        # Open the group that should be open.
        self.open_target_group_for_form(form)
        content = self.get_rendered_fields(form, context, template_pack)
        links = SafeString("".join(tab.render_link(template_pack) for tab in self.fields))

        context.update({"tabs": self, "links": links, "content": content})
        template = self.get_template_name(template_pack)
        return render_to_string(template, context.flatten())


class AccordionGroup(Container):
    """
    Accordion Group (pane) object. It wraps given fields inside an accordion
    tab. It takes accordion tab name as first argument.

    Tab object. It wraps fields in a div whose default class is "tab-pane" and
    takes a name as first argument.

    Attributes
    ----------
    template : str
        The default template which this Layout Object will be rendered
        with.
    css_class : str, optional
        CSS classes to be applied to the ``<div>``. By default "".

    Parameters
    ----------
    name : str
        The name of the container.
    *fields : str, LayoutObject
        Any number of fields as positional arguments to be rendered within
        the container.
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
    Example::

        AccordionGroup("group name", "form_field_1", "form_field_2")
    """

    template = "%s/accordion-group.html"
    data_parent = ""  # accordion parent div id.


class Accordion(ContainerHolder):
    """
    Accordion menu object. It wraps `AccordionGroup` objects in a container

    Attributes
    ----------
    template : str
        The default template which this Layout Object will be rendered
        with.
    css_class : str, optional
        CSS classes to be applied to the ``<div>``. By default None.

    Parameters
    ----------
    *accordion_groups : str, LayoutObject
        Any number of layout objects as positional arguments to be rendered
        within the ``<div>``.
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

    Example::

        Accordion(
            AccordionGroup("group name", "form_field_1", "form_field_2"),
            AccordionGroup("another group name", "form_field")
        )
    """

    template = "%s/accordion.html"

    def __init__(self, *accordion_groups, css_id=None, css_class=None, template=None, **kwargs):
        super().__init__(*accordion_groups, css_id=css_id, css_class=css_class, template=template, **kwargs)

        # Accordion needs to have a unique id
        if not self.css_id:
            self.css_id = "-".join(["accordion", str(randint(1000, 9999))])

        # AccordionGroup need to have 'data-parent="#Accordion.id"'
        for accordion_group in accordion_groups:
            accordion_group.data_parent = self.css_id

    def render(self, form, context, template_pack=TEMPLATE_PACK, **kwargs):
        content = SafeString("")

        # Open the group that should be open.
        self.open_target_group_for_form(form)

        for group in self.fields:
            group.data_parent = self.css_id
            content += render_field(group, form, context, template_pack=template_pack, **kwargs)

        template = self.get_template_name(template_pack)
        context.update({"accordion": self, "content": content})

        return render_to_string(template, context.flatten())


class Alert(Div):
    """
    Generates markup in the form of an alert dialog.

    Attributes
    ----------
    template: str
        The default template which this Layout Object will be rendered
        with.
    css_class : str
        The CSS classes to be applied to the alert. By defult "alert".

    Parameters
    ----------
    content : str
        The content of the alert.
    dismiss : bool
        If true the alert contains a button to dismiss the alert. By default
        True.
    block : str, optional
        Additional CSS classes to be applied to the ``<button>``. By default
        None.
    css_id : str, optional
        A DOM id for the layout object which will be added to the alert if
        provided. By default None.
    css_class : str, optional
        Additional CSS classes to be applied in addition to those declared by
        the class itself. By default None.
    template : str, optional
        Overrides the default template, if provided. By default None.
    **kwargs : dict, optional
        Additional attributes are passed to ``flatatt`` and converted into
        key="value", pairs. These attributes are then available in the template
        context.

    Examples
    --------

    Example::

        Alert(content='<strong>Warning!</strong> Best check yo self, you're not looking too good.')

    """

    template = "%s/layout/alert.html"
    css_class = "alert"

    def __init__(self, content, dismiss=True, block=False, css_id=None, css_class=None, template=None, **kwargs):
        fields = []
        if block:
            self.css_class += " alert-block"
        super().__init__(*fields, css_id=css_id, css_class=css_class, template=template, **kwargs)
        self.content = content
        self.dismiss = dismiss

    def render(self, form, context, template_pack=TEMPLATE_PACK, **kwargs):
        template = self.get_template_name(template_pack)
        context.update({"alert": self, "content": self.content, "dismiss": self.dismiss})

        return render_to_string(template, context.flatten())


class UneditableField(Field):
    """
    Layout object for rendering fields as uneditable in bootstrap.

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
    fields : str
        The name of the field.
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

        UneditableField('field_name', css_class="input-xlarge")
    """

    template = "%s/layout/uneditable_input.html"

    def __init__(self, field, css_class=None, wrapper_class=None, template=None, **kwargs):
        self.attrs = {"class": "uneditable-input"}
        super().__init__(field, css_class=css_class, wrapper_class=wrapper_class, template=template, **kwargs)


class InlineField(Field):
    """
    Layout object for rendering fields as Inline in bootstrap.

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

        InlineField('field_name')
    """

    template = "%s/layout/inline_field.html"


class Modal(LayoutObject):
    """
    Boostrap layout object for rendering crispy forms objects inside a
    bootstrap modal.

    Attributes
    ----------
    template : str
        The default template which this Layout Object will be rendered
        with.

    Parameters
    ----------
    *fields : str
        The fields to be rendered within the modal.
    template : str, optional
        Overrides the default template, if provided. By default ``None``.
    css_id: str, optional
        The modal's DOM id. By default ``modal_id``.
    title: str, optional
        Text to display in the modal's header which will be wrapped in an
        ``<H5>`` tag. By default ``Modal Title``.
    title_id: str, optional
        The title's DOM id. By default ``modal_title_id``.
    css_class : str, optional
        CSS classes to be applied to the field. These are added to any classes
        included in the ``attrs`` dict. By default None.
    title_class: str, optional
        Additional CSS classes to be applied to the title. By default None.
    **kwargs : dict, optional
        Additional attributes are converted into key="value", pairs. These
        attributes are added to the ``<div>``.

    Examples
    --------

    Example::

        Modal(
            'field1',
            Div('field2'),
            css_id="modal-id-ex",
            css_class="modal-class-ex,
            title="This is my modal",
        )
    """

    template = "%s/layout/modal.html"

    def __init__(
        self,
        *fields,
        template=None,
        css_id="modal_id",
        title="Modal Title",
        title_id="modal_title_id",
        css_class=None,
        title_class=None,
        **kwargs,
    ):
        self.fields = list(fields)
        self.template = template or self.template
        self.css_id = css_id
        self.css_class = css_class or ""
        self.title = title
        self.title_id = title_id
        self.title_class = title_class or ""

        kwargs = {**kwargs, "tabindex": "-1", "role": "dialog", "aria-labelledby": "%s-label" % self.title_id}

        self.flat_attrs = flatatt(kwargs)

    def render(self, form, context, template_pack=TEMPLATE_PACK, **kwargs):
        fields = self.get_rendered_fields(form, context, template_pack, **kwargs)
        template = self.get_template_name(template_pack)

        return render_to_string(template, {"modal": self, "fields": fields})
