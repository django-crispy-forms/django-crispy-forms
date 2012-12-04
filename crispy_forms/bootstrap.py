import warnings

from django.template import Context, Template
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.forms.util import flatatt

from .layout import LayoutObject, Field, Div
from .utils import render_field


class AppendedText(Field):
    template = "bootstrap/layout/appended_text.html"

    def __init__(self, field, text, *args, **kwargs):
        self.field = field
        self.text = text
        if 'active' in kwargs:
            self.active = kwargs.pop('active')

        super(AppendedText, self).__init__(field, *args, **kwargs)

    def render(self, form, form_style, context, template_pack='bootstrap'):
        context.update({'crispy_appended_text': self.text, 'active': getattr(self, "active", False)})
        return render_field(self.field, form, form_style, context, template=self.template, attrs=self.attrs, template_pack=template_pack)


class PrependedText(AppendedText):
    template = "bootstrap/layout/prepended_text.html"

    def render(self, form, form_style, context, template_pack='bootstrap'):
        context.update({'crispy_prepended_text': self.text, 'active': getattr(self, "active", False)})
        return render_field(self.field, form, form_style, context, template=self.template, attrs=self.attrs, template_pack=template_pack)


class PrependedAppendedText(Field):
    template = "bootstrap/layout/appended_prepended_text.html"

    def __init__(self, field, prepended_text=None, appended_text=None, *args, **kwargs):
        self.field = field
        self.appended_text = appended_text
        self.prepended_text = prepended_text
        if 'active' in kwargs:
            self.active = kwargs.pop('active')

        super(PrependedAppendedText, self).__init__(field, *args, **kwargs)

    def render(self, form, form_style, context, template_pack='bootstrap'):
        context.update({'crispy_appended_text': self.appended_text,
                        'crispy_prepended_text': self.prepended_text,
                        'active': getattr(self, "active", False)})
        return render_field(self.field, form, form_style, context, template=self.template, attrs=self.attrs, template_pack=template_pack)


class AppendedPrependedText(PrependedAppendedText):
    def __init__(self, *args, **kwargs):
        warnings.warn("AppendedPrependedText has been renamed to PrependedAppendedText, \
            it will be removed in 1.3.0", PendingDeprecationWarning)
        super(AppendedPrependedText, self).__init__(*args, **kwargs)


class FormActions(LayoutObject):
    """
    Bootstrap layout object. It wraps fields in a <div class="form-actions">

    Example::

        FormActions(
            HTML(<span style="display: hidden;">Information Saved</span>),
            Submit('Save', 'Save', css_class='btn-primary')
        )
    """
    template = "bootstrap/layout/formactions.html"

    def __init__(self, *fields, **kwargs):
        self.fields = list(fields)
        self.template = kwargs.pop('template', self.template)
        self.attrs = kwargs
        if 'css_class' in self.attrs:
            self.attrs['class'] = self.attrs.pop('css_class')

    def render(self, form, form_style, context, template_pack='bootstrap'):
        html = u''
        for field in self.fields:
            html += render_field(field, form, form_style, context, template_pack=template_pack)

        return render_to_string(self.template, Context({'formactions': self, 'fields_output': html}))

    def flat_attrs(self):
        return flatatt(self.attrs)


class InlineCheckboxes(Field):
    """
    Layout object for rendering checkboxes inline::

        InlineCheckboxes('field_name')
    """
    template = "bootstrap/layout/checkboxselectmultiple_inline.html"

    def render(self, form, form_style, context, template_pack='bootstrap'):
        context.update({'inline_class': 'inline'})
        html = super(InlineCheckboxes, self).render(form, form_style, context)
        # We delete the inserted key to avoid side effects
        del context.dicts[-2]['inline_class']
        return html


class InlineRadios(Field):
    """
    Layout object for rendering radiobuttons inline::

        InlineRadios('field_name')
    """
    template = "bootstrap/layout/radioselect_inline.html"

    def render(self, form, form_style, context, template_pack='bootstrap'):
        context.update({'inline_class': 'inline'})
        html = super(InlineRadios, self).render(form, form_style, context)
        # We delete the inserted key to avoid side effects
        del context.dicts[-2]['inline_class']
        return html


class FieldWithButtons(Div):
    template = 'bootstrap/layout/field_with_buttons.html'

    def render(self, form, form_style, context):
        # We first render the buttons
        buttons = ''
        for field in self.fields[1:]:
            buttons += render_field(field, form, form_style, context,
                'bootstrap/layout/field.html', layout_object=self)

        context.update({'div': self, 'buttons': buttons})

        if isinstance(self.fields[0], Field):
            # FieldWithButtons(Field('field_name'), StrictButton("go"))
            # We render the field passing its name and attributes
            return render_field(self.fields[0][0], form, form_style, context,
                self.template, attrs=self.fields[0].attrs)
        else:
            return render_field(self.fields[0], form, form_style, context, self.template)


class StrictButton(object):
    """
    Layout oject for rendering an HTML button::

        Button("button content", css_class="extra")
    """
    template = 'bootstrap/layout/button.html'
    field_classes = 'btn'

    def __init__(self, content, **kwargs):
        self.content = content
        self.template = kwargs.pop('template', self.template)

        kwargs.setdefault('type', 'button')

        # We turn css_id and css_class into id and class
        if kwargs.has_key('css_id'):
            kwargs['id'] = kwargs.pop('css_id')
        kwargs['class'] = self.field_classes
        if kwargs.has_key('css_class'):
            kwargs['class'] += " %s" % kwargs.pop('css_class')

        self.flat_attrs = flatatt(kwargs)

    def render(self, form, form_style, context):
        self.content = Template(unicode(self.content)).render(context)
        return render_to_string(self.template, Context({'button': self}))


class Tab(Div):
    """
    Tab object. It wraps fields in a div whose default class is "tab-pane" and
    takes a name as first argument. Example::

        Tab('tab_name', 'form_field_1', 'form_field_2', 'form_field_3')
    """
    css_class = 'tab-pane'
    link_template = 'bootstrap/layout/tab-link.html'

    def __init__(self, name, *fields, **kwargs):
        super(Tab, self).__init__(*fields, **kwargs)
        self.name = name
        self.active = False
        # id is necessary for the TabHolder links
        if not self.css_id:
            self.css_id = slugify(self.name)

    def __contains__(self, field_name):
        """
        check if field_name is contained within tab.
        """
        return field_name in map(lambda pointer: pointer[1], self.get_field_names())

    def render_link(self):
        """
        Render the link for the tab-pane. It must be called after render so css_class is updated
        with active if needed.
        """
        return render_to_string(self.link_template, Context({'link': self}))

    def render(self, form, form_style, context):
        if self.active:
            self.css_class += ' active'
        return super(Tab, self).render(form, form_style, context)


class TabHolder(Div):
    """
    TabHolder object. It wraps Tab objects in a container. Requiers bootstrap-tab.js::

            TabHolder(Tab('form_field_1', 'form_field_2'), Tab('form_field_3'))
    """
    template = 'bootstrap/layout/tab.html'
    css_class = 'nav nav-tabs'

    def first_tab_with_errors(self, errors):
        """
        Returns the first tab with errors, otherwise returns the first tab
        """
        for tab in self.fields:
            errors_here = bool(filter(lambda error: error in tab, errors))
            if errors_here:
                return tab

        return self.fields[0]

    def render(self, form, form_style, context, template_pack='bootstrap'):
        links, content = '', ''
        self.first_tab_with_errors(form.errors.keys()).active = True
        for tab in self.fields:
            content += render_field(tab, form, form_style, context,
                                    template_pack=template_pack)
            links += tab.render_link()
        return render_to_string(self.template,
            Context({'tabs': self, 'links': links, 'content': content}))
