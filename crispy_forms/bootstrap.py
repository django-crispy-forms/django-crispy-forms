from django.template import Context
from django.template.loader import render_to_string
from django.forms.util import flatatt

from layout import LayoutObject, Field
from utils import render_field


class AppendedText(Field):
    template = "bootstrap/layout/appended_text.html"

    def __init__(self, field, text, *args, **kwargs):
        self.field = field
        self.text = text
        if 'active' in kwargs:
            self.active = kwargs.pop('active')

        super(AppendedText, self).__init__(field, *args, **kwargs)

    def render(self, form, form_style, context):
        context.update({'crispy_appended_text': self.text, 'active': getattr(self, "active", False)})
        return render_field(self.field, form, form_style, context, template=self.template, attrs=self.attrs)


class PrependedText(AppendedText):
    template = "bootstrap/layout/prepended_text.html"

    def render(self, form, form_style, context):
        context.update({'crispy_prepended_text': self.text, 'active': getattr(self, "active", False)})
        return render_field(self.field, form, form_style, context, template=self.template, attrs=self.attrs)


class AppendedPrependedText(Field):
    template = "bootstrap/layout/appended_prepended_text.html"

    def __init__(self, field, prepended_text=None, appended_text=None, *args, **kwargs):
        self.field = field
        self.appended_text = appended_text
        self.prepended_text = prepended_text
        if 'active' in kwargs:
            self.active = kwargs.pop('active')

        super(AppendedPrependedText, self).__init__(field, *args, **kwargs)

    def render(self, form, form_style, context):
        context.update({'crispy_appended_text': self.appended_text,
                        'crispy_prepended_text': self.prepended_text,
                        'active': getattr(self, "active", False)})
        return render_field(self.field, form, form_style, context, template=self.template, attrs=self.attrs)


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

    def render(self, form, form_style, context):
        html = u''
        for field in self.fields:
            html += render_field(field, form, form_style, context)

        return render_to_string(self.template, Context({'formactions': self, 'fields_output': html}))

    def flat_attrs(self):
        return flatatt(self.attrs)


class InlineCheckboxes(Field):
    """
    Layout object for rendering checkboxes inline::

        InlineCheckboxes('field_name')
    """
    template = "bootstrap/layout/checkboxselectmultiple_inline.html"

    def render(self, form, form_style, context):
        context.update({'inline_class': 'inline'})
        html = super(InlineCheckboxes, self).render(form, form_style, context)
        # We delete the inserted key to avoid side effects
        del context.dicts[-2]['inline_class']
        return html
