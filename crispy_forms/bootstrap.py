from random import randint

from django.template import Template
from django.template.loader import render_to_string
from django.utils.text import slugify

from .layout import Div, Field, LayoutObject, TemplateNameMixin
from .utils import TEMPLATE_PACK, flatatt, render_field


class PrependedAppendedText(Field):
    template = "%s/layout/prepended_appended_text.html"

    def __init__(self, field, prepended_text=None, appended_text=None, input_size=None, *args, **kwargs):
        self.field = field
        self.appended_text = appended_text
        self.prepended_text = prepended_text
        if "active" in kwargs:
            self.active = kwargs.pop("active")

        self.input_size = input_size
        css_class = kwargs.get("css_class", "")

        # Bootstrap 3
        if "input-lg" in css_class:
            self.input_size = "input-lg"
        if "input-sm" in css_class:
            self.input_size = "input-sm"

        super().__init__(field, *args, **kwargs)

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, extra_context=None, **kwargs):
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
            form_style,
            context,
            template=template,
            attrs=self.attrs,
            template_pack=template_pack,
            extra_context=extra_context,
            **kwargs,
        )


class AppendedText(PrependedAppendedText):
    def __init__(self, field, text, *args, **kwargs):
        kwargs.pop("appended_text", None)
        kwargs.pop("prepended_text", None)
        self.text = text
        super().__init__(field, appended_text=text, **kwargs)


class PrependedText(PrependedAppendedText):
    def __init__(self, field, text, *args, **kwargs):
        kwargs.pop("appended_text", None)
        kwargs.pop("prepended_text", None)
        self.text = text
        super().__init__(field, prepended_text=text, **kwargs)


class FormActions(LayoutObject):
    """
    Bootstrap layout object. It wraps fields in a <div class="form-actions">

    Example::

        FormActions(
            HTML(<span style="display: hidden;">Information Saved</span>),
            Submit('Save', 'Save', css_class='btn-primary')
        )
    """

    template = "%s/layout/formactions.html"

    def __init__(self, *fields, **kwargs):
        self.fields = list(fields)
        self.template = kwargs.pop("template", self.template)
        self.attrs = kwargs
        if "css_class" in self.attrs:
            self.attrs["class"] = self.attrs.pop("css_class")

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        html = self.get_rendered_fields(form, form_style, context, template_pack, **kwargs)
        template = self.get_template_name(template_pack)
        context.update({"formactions": self, "fields_output": html})

        return render_to_string(template, context.flatten())

    def flat_attrs(self):
        return flatatt(self.attrs)


class InlineCheckboxes(Field):
    """
    Layout object for rendering checkboxes inline::

        InlineCheckboxes('field_name')
    """

    template = "%s/layout/checkboxselectmultiple_inline.html"

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        return super().render(
            form, form_style, context, template_pack=template_pack, extra_context={"inline_class": "inline"}
        )


class InlineRadios(Field):
    """
    Layout object for rendering radiobuttons inline::

        InlineRadios('field_name')
    """

    template = "%s/layout/radioselect_inline.html"

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        return super().render(
            form, form_style, context, template_pack=template_pack, extra_context={"inline_class": "inline"}
        )


class FieldWithButtons(Div):
    """
    A layout object for rendering a single field with any number of buttons.

    Args:
        fields : str or LayoutObject
            The first positional argument is the field. This can be either the
            name of the field as a string or an instance of `Field`. Following
            arguments will be rendered as buttons.
        input_size : str
            Additional CSS class to change the size of the input. e.g.
            "input-group-sm".
        kwargs
            Additional kwargs to be passed to the parent `Div` Layout Object.

    Example::

        FieldWithButtons(
            Field("password1", css_class="span4"),
            StrictButton("Go!", css_id="go-button"),
            input_size="input-group-sm",
        )
    """

    template = "%s/layout/field_with_buttons.html"
    field_template = "%s/field.html"

    def __init__(self, *fields, input_size=None, **kwargs):
        self.input_size = input_size
        super().__init__(*fields, **kwargs)

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, extra_context=None, **kwargs):
        # We first render the buttons
        field_template = self.field_template % template_pack
        buttons = "".join(
            render_field(
                field,
                form,
                form_style,
                context,
                field_template,
                layout_object=self,
                template_pack=template_pack,
                **kwargs,
            )
            for field in self.fields[1:]
        )

        extra_context = {"div": self, "buttons": buttons}
        template = self.get_template_name(template_pack)

        if isinstance(self.fields[0], Field):
            # FieldWithButtons(Field('field_name'), StrictButton("go"))
            # We render the field passing its name and attributes
            return render_field(
                self.fields[0][0],
                form,
                form_style,
                context,
                template,
                attrs=self.fields[0].attrs,
                template_pack=template_pack,
                extra_context=extra_context,
                **kwargs,
            )
        else:
            return render_field(
                self.fields[0], form, form_style, context, template, extra_context=extra_context, **kwargs
            )


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

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        self.content = Template(str(self.content)).render(context)
        template = self.get_template_name(template_pack)
        context.update({"button": self})

        return render_to_string(template, context.flatten())


class Container(Div):
    """
    Base class used for `Tab` and `AccordionGroup`, represents a basic container concept
    """

    css_class = ""

    def __init__(self, name, *fields, **kwargs):
        super().__init__(*fields, **kwargs)
        self.template = kwargs.pop("template", self.template)
        self.name = name
        self._active_originally_included = "active" in kwargs
        self.active = kwargs.pop("active", False)
        if not self.css_id:
            self.css_id = slugify(self.name, allow_unicode=True)

    def __contains__(self, field_name):
        """
        check if field_name is contained within tab.
        """
        return field_name in map(lambda pointer: pointer[1], self.get_field_names())

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        if self.active:
            if "active" not in self.css_class:
                self.css_class += " active"
        else:
            self.css_class = self.css_class.replace("active", "")
        return super().render(form, form_style, context, template_pack)


class ContainerHolder(Div):
    """
    Base class used for `TabHolder` and `Accordion`, groups containers
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
    takes a name as first argument. Example::

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


class TabHolder(ContainerHolder):
    """
    TabHolder object. It wraps Tab objects in a container. Requires bootstrap-tab.js::

        TabHolder(
            Tab('form_field_1', 'form_field_2'),
            Tab('form_field_3')
        )
    """

    template = "%s/layout/tab.html"

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        for tab in self.fields:
            tab.active = False

        # Open the group that should be open.
        self.open_target_group_for_form(form)
        content = self.get_rendered_fields(form, form_style, context, template_pack)
        links = "".join(tab.render_link(template_pack) for tab in self.fields)

        context.update({"tabs": self, "links": links, "content": content})
        template = self.get_template_name(template_pack)
        return render_to_string(template, context.flatten())


class AccordionGroup(Container):
    """
    Accordion Group (pane) object. It wraps given fields inside an accordion
    tab. It takes accordion tab name as first argument::

        AccordionGroup("group name", "form_field_1", "form_field_2")
    """

    template = "%s/accordion-group.html"
    data_parent = ""  # accordion parent div id.


class Accordion(ContainerHolder):
    """
    Accordion menu object. It wraps `AccordionGroup` objects in a container::

        Accordion(
            AccordionGroup("group name", "form_field_1", "form_field_2"),
            AccordionGroup("another group name", "form_field")
        )
    """

    template = "%s/accordion.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Accordion needs to have a unique id
        if not self.css_id:
            self.css_id = "-".join(["accordion", str(randint(1000, 9999))])

        # AccordionGroup need to have 'data-parent="#Accordion.id"'
        for accordion_group in args:
            accordion_group.data_parent = self.css_id

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        content = ""

        # Open the group that should be open.
        self.open_target_group_for_form(form)

        for group in self.fields:
            group.data_parent = self.css_id
            content += render_field(group, form, form_style, context, template_pack=template_pack, **kwargs)

        template = self.get_template_name(template_pack)
        context.update({"accordion": self, "content": content})

        return render_to_string(template, context.flatten())


class Alert(Div):
    """
    `Alert` generates markup in the form of an alert dialog

        Alert(content='<strong>Warning!</strong> Best check yo self, you're not looking too good.')
    """

    template = "%s/layout/alert.html"
    css_class = "alert"

    def __init__(self, content, dismiss=True, block=False, **kwargs):
        fields = []
        if block:
            self.css_class += " alert-block"
        Div.__init__(self, *fields, **kwargs)
        self.template = kwargs.pop("template", self.template)
        self.content = content
        self.dismiss = dismiss

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        template = self.get_template_name(template_pack)
        context.update({"alert": self, "content": self.content, "dismiss": self.dismiss})

        return render_to_string(template, context.flatten())


class UneditableField(Field):
    """
    Layout object for rendering fields as uneditable in bootstrap

    Example::

        UneditableField('field_name', css_class="input-xlarge")
    """

    template = "%s/layout/uneditable_input.html"

    def __init__(self, field, *args, **kwargs):
        self.attrs = {"class": "uneditable-input"}
        super().__init__(field, *args, **kwargs)


class InlineField(Field):
    template = "%s/layout/inline_field.html"


class Modal(LayoutObject):
    """
    Boostrap layout object for rendering crispy forms objects inside a bootstrap modal.

    The following attributes can be set:
        - `css_id`: modal's DOM id
        - `css_class`: modal's DOM classes
            - NOTE: "modal" and "fade" are applied by default on the template
        - `title`: text to display in the modal's header
            - NOTE: text will be wrapped in a <h5> tag
        - `title_id`: title's DOM id
        - `title_class`: titles's DOM classes
            - NOTE: "modal-title" is applied by default on the template
        - template
            The default template which this Layout Object will be rendered
            with

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
        css_class="",
        title_class="",
        **kwargs,
    ):

        self.fields = list(fields)
        self.template = template or self.template
        self.css_id = css_id
        self.css_class = css_class
        self.title = title
        self.title_id = title_id
        self.title_class = title_class

        kwargs = {**kwargs, "tabindex": "-1", "role": "dialog", "aria-labelledby": "%s-label" % self.title_id}

        self.flat_attrs = flatatt(kwargs)

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        fields = self.get_rendered_fields(form, form_style, context, template_pack, **kwargs)
        template = self.get_template_name(template_pack)

        return render_to_string(template, {"modal": self, "fields": fields})
