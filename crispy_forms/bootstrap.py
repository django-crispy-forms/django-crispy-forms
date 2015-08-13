from random import randint

from django.template import Context, Template
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

from .compatibility import text_type
from .layout import LayoutObject, Field, Div
from .utils import render_field, flatatt, TEMPLATE_PACK



class PrependedAppendedText(Field):
    template = "%s/layout/prepended_appended_text.html"

    def __init__(self, field, prepended_text=None, appended_text=None, *args, **kwargs):
        self.field = field
        self.appended_text = appended_text
        self.prepended_text = prepended_text
        if 'active' in kwargs:
            self.active = kwargs.pop('active')

        self.input_size = None
        css_class = kwargs.get('css_class', '')
        if css_class.find('input-lg') != -1: self.input_size = 'input-lg'
        if css_class.find('input-sm') != -1: self.input_size = 'input-sm'

        super(PrependedAppendedText, self).__init__(field, *args, **kwargs)

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, extra_context=None, **kwargs):
        extra_context = {
            'crispy_appended_text': self.appended_text,
            'crispy_prepended_text': self.prepended_text,
            'input_size' : self.input_size,
            'active': getattr(self, "active", False)
        }
        template = self.template % template_pack
        return render_field(
            self.field, form, form_style, context,
            template=template, attrs=self.attrs,
            template_pack=template_pack, extra_context=extra_context, **kwargs
        )


class AppendedText(PrependedAppendedText):
    def __init__(self, field, text, *args, **kwargs):
        kwargs.pop('appended_text', None)
        kwargs.pop('prepended_text', None)
        self.text = text
        super(AppendedText, self).__init__(field, appended_text=text, **kwargs)


class PrependedText(PrependedAppendedText):
    def __init__(self, field, text, *args, **kwargs):
        kwargs.pop('appended_text', None)
        kwargs.pop('prepended_text', None)
        self.text = text
        super(PrependedText, self).__init__(field, prepended_text=text, **kwargs)


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
        self.template = kwargs.pop('template', self.template)
        self.attrs = kwargs
        if 'css_class' in self.attrs:
            self.attrs['class'] = self.attrs.pop('css_class')

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        html = u''
        for field in self.fields:
            html += render_field(field, form, form_style, context, template_pack=template_pack, **kwargs)
        extra_context = {
            'formactions': self,
            'fields_output': html
        }
        template = self.template % template_pack
        return render_to_string(template, extra_context, context)

    def flat_attrs(self):
        return flatatt(self.attrs)


class InlineCheckboxes(Field):
    """
    Layout object for rendering checkboxes inline::

        InlineCheckboxes('field_name')
    """
    template = "%s/layout/checkboxselectmultiple_inline.html"

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        return super(InlineCheckboxes, self).render(
            form, form_style, context, template_pack=template_pack,
            extra_context={'inline_class': 'inline'}
        )


class InlineRadios(Field):
    """
    Layout object for rendering radiobuttons inline::

        InlineRadios('field_name')
    """
    template = "%s/layout/radioselect_inline.html"

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        return super(InlineRadios, self).render(
            form, form_style, context, template_pack=template_pack,
            extra_context={'inline_class': 'inline'}
        )


class FieldWithButtons(Div):
    template = '%s/layout/field_with_buttons.html'
    field_template = '%s/layout/field.html'

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, extra_context=None, **kwargs):
        # We first render the buttons
        buttons = ''
        field_template = self.field_template % template_pack
        for field in self.fields[1:]:
            buttons += render_field(
                field, form, form_style, context,
                field_template, layout_object=self,
                template_pack=template_pack, **kwargs
            )

        extra_context = {'div': self, 'buttons': buttons}
        template = self.template % template_pack

        if isinstance(self.fields[0], Field):
            # FieldWithButtons(Field('field_name'), StrictButton("go"))
            # We render the field passing its name and attributes
            return render_field(
                self.fields[0][0], form, form_style, context,
                template, attrs=self.fields[0].attrs,
                template_pack=template_pack, extra_context=extra_context, **kwargs
            )
        else:
            return render_field(
                self.fields[0], form, form_style, context, template,
                extra_context=extra_context, **kwargs
            )


class StrictButton(object):
    """
    Layout oject for rendering an HTML button::

        Button("button content", css_class="extra")
    """
    template = '%s/layout/button.html'
    field_classes = 'btn'

    def __init__(self, content, **kwargs):
        self.content = content
        self.template = kwargs.pop('template', self.template)

        kwargs.setdefault('type', 'button')

        # We turn css_id and css_class into id and class
        if 'css_id' in kwargs:
            kwargs['id'] = kwargs.pop('css_id')
        kwargs['class'] = self.field_classes
        if 'css_class' in kwargs:
            kwargs['class'] += " %s" % kwargs.pop('css_class')

        self.flat_attrs = flatatt(kwargs)

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        self.content = Template(text_type(self.content)).render(context)
        template = self.template % template_pack
        return render_to_string(template, {'button': self}, context)


class Container(Div):
    """
    Base class used for `Tab` and `AccordionGroup`, represents a basic container concept
    """
    css_class = ""

    def __init__(self, name, *fields, **kwargs):
        super(Container, self).__init__(*fields, **kwargs)
        self.template = kwargs.pop('template', self.template)
        self.name = name
        self._active_originally_included = "active" in kwargs
        self.active = kwargs.pop("active", False)
        if not self.css_id:
            self.css_id = slugify(self.name)

    def __contains__(self, field_name):
        """
        check if field_name is contained within tab.
        """
        return field_name in map(lambda pointer: pointer[1], self.get_field_names())

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        if self.active:
            if not 'active' in self.css_class:
                self.css_class += ' active'
        else:
            self.css_class = self.css_class.replace('active', '')
        return super(Container, self).render(form, form_style, context, template_pack)


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
            if not target._active_originally_included:
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
    css_class = 'tab-pane'
    link_template = '%s/layout/tab-link.html'

    def render_link(self, template_pack=TEMPLATE_PACK, **kwargs):
        """
        Render the link for the tab-pane. It must be called after render so css_class is updated
        with active if needed.
        """
        link_template = self.link_template % template_pack
        return render_to_string(link_template, {'link': self})


class TabHolder(ContainerHolder):
    """
    TabHolder object. It wraps Tab objects in a container. Requires bootstrap-tab.js::

        TabHolder(
            Tab('form_field_1', 'form_field_2'),
            Tab('form_field_3')
        )
    """
    template = '%s/layout/tab.html'

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        links, content = '', ''
        for tab in self.fields:
            tab.active = False

        # Open the group that should be open.
        self.open_target_group_for_form(form)

        for tab in self.fields:
            content += render_field(
                tab, form, form_style, context, template_pack=template_pack, **kwargs
            )
            links += tab.render_link(template_pack)

        extra_context = {
            'tabs': self,
            'links': links,
            'content': content
        }
        template = self.template % template_pack
        return render_to_string(template, extra_context, context)


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

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        content = ''

        # accordion group needs the parent div id to set `data-parent` (I don't
        # know why). This needs to be a unique id
        if not self.css_id:
            self.css_id = "-".join(["accordion", text_type(randint(1000, 9999))])

        # Open the group that should be open.
        self.open_target_group_for_form(form)

        for group in self.fields:
            group.data_parent = self.css_id
            content += render_field(
                group, form, form_style, context, template_pack=template_pack, **kwargs
            )

        template = self.template % template_pack
        return render_to_string(
            template,
            {'accordion': self, 'content': content},
            context
        )


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
            self.css_class += ' alert-block'
        Div.__init__(self, *fields, **kwargs)
        self.template = kwargs.pop('template', self.template)
        self.content = content
        self.dismiss = dismiss

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        template = self.template % template_pack
        return render_to_string(
            template,
            {'alert': self, 'content': self.content, 'dismiss': self.dismiss},
            context
        )


class UneditableField(Field):
    """
    Layout object for rendering fields as uneditable in bootstrap

    Example::

        UneditableField('field_name', css_class="input-xlarge")
    """
    template = "%s/layout/uneditable_input.html"

    def __init__(self, field, *args, **kwargs):
        self.attrs = {'class': 'uneditable-input'}
        super(UneditableField, self).__init__(field, *args, **kwargs)


class InlineField(Field):
    template = "%s/layout/inline_field.html"
