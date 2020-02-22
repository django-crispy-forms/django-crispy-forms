from django import template
from django.conf import settings
from django.forms.formsets import BaseFormSet
from django.template.loader import get_template

from crispy_forms.compatibility import lru_cache
from crispy_forms.helper import FormHelper
from crispy_forms.utils import TEMPLATE_PACK, get_template_pack

register = template.Library()

# We import the filters, so they are available when doing load crispy_forms_tags
from crispy_forms.templatetags.crispy_forms_filters import *  # NOQA: F403,F401 isort:skip


class ForLoopSimulator:
    """
    Simulates a forloop tag, precisely::

        {% for form in formset.forms %}

    If `{% crispy %}` is rendering a formset with a helper, We inject a `ForLoopSimulator` object
    in the context as `forloop` so that formset forms can do things like::

        Fieldset("Item {{ forloop.counter }}", [...])
        HTML("{% if forloop.first %}First form text{% endif %}"
    """

    def __init__(self, formset):
        self.len_values = len(formset.forms)

        # Shortcuts for current loop iteration number.
        self.counter = 1
        self.counter0 = 0
        # Reverse counter iteration numbers.
        self.revcounter = self.len_values
        self.revcounter0 = self.len_values - 1
        # Boolean values designating first and last times through loop.
        self.first = True
        self.last = 0 == self.len_values - 1

    def iterate(self):
        """
        Updates values as if we had iterated over the for
        """
        self.counter += 1
        self.counter0 += 1
        self.revcounter -= 1
        self.revcounter0 -= 1
        self.first = False
        self.last = self.revcounter0 == self.len_values - 1


class BasicNode(template.Node):
    """
    Basic Node object that we can rely on for Node objects in normal
    template tags. I created this because most of the tags we'll be using
    will need both the form object and the helper string. This handles
    both the form object and parses out the helper string into attributes
    that templates can easily handle.
    """

    def __init__(self, form, helper, template_pack=None):
        self.form = form
        if helper is not None:
            self.helper = helper
        else:
            self.helper = None
        self.template_pack = template_pack or get_template_pack()

    def get_render(self, context):
        """
        Returns a `Context` object with all the necessary stuff for rendering the form

        :param context: `django.template.Context` variable holding the context for the node

        `self.form` and `self.helper` are resolved into real Python objects resolving them
        from the `context`. The `actual_form` can be a form or a formset. If it's a formset
        `is_formset` is set to True. If the helper has a layout we use it, for rendering the
        form or the formset's forms.
        """
        # Nodes are not thread safe in multithreaded environments
        # https://docs.djangoproject.com/en/dev/howto/custom-template-tags/#thread-safety-considerations
        if self not in context.render_context:
            context.render_context[self] = (
                template.Variable(self.form),
                template.Variable(self.helper) if self.helper else None,
            )
        form, helper = context.render_context[self]

        actual_form = form.resolve(context)
        if self.helper is not None:
            helper = helper.resolve(context)
        else:
            # If the user names the helper within the form `helper` (standard), we use it
            # This allows us to have simplified tag syntax: {% crispy form %}
            helper = FormHelper() if not hasattr(actual_form, "helper") else actual_form.helper

        # use template_pack from helper, if defined
        try:
            if helper.template_pack:
                self.template_pack = helper.template_pack
        except AttributeError:
            pass

        self.actual_helper = helper

        # We get the response dictionary
        is_formset = isinstance(actual_form, BaseFormSet)
        response_dict = self.get_response_dict(helper, context, is_formset)
        node_context = context.__copy__()
        node_context.update({"is_bound": actual_form.is_bound})
        node_context.update(response_dict)
        final_context = node_context.__copy__()

        # If we have a helper's layout we use it, for the form or the formset's forms
        if helper and helper.layout:
            if not is_formset:
                actual_form.form_html = helper.render_layout(
                    actual_form, node_context, template_pack=self.template_pack
                )
            else:
                forloop = ForLoopSimulator(actual_form)
                helper.render_hidden_fields = True
                for form in actual_form:
                    node_context.update({"forloop": forloop})
                    node_context.update({"formset_form": form})
                    form.form_html = helper.render_layout(form, node_context, template_pack=self.template_pack)
                    forloop.iterate()

        if is_formset:
            final_context["formset"] = actual_form
        else:
            final_context["form"] = actual_form

        return final_context

    def get_response_dict(self, helper, context, is_formset):
        """
        Returns a dictionary with all the parameters necessary to render the form/formset in a template.

        :param context: `django.template.Context` for the node
        :param is_formset: Boolean value. If set to True, indicates we are working with a formset.
        """
        if not isinstance(helper, FormHelper):
            raise TypeError("helper object provided to {% crispy %} tag must be a crispy.helper.FormHelper object.")

        attrs = helper.get_attributes(template_pack=self.template_pack)
        form_type = "form"
        if is_formset:
            form_type = "formset"

        # We take form/formset parameters from attrs if they are set, otherwise we use defaults
        response_dict = {
            "%s_action" % form_type: attrs["attrs"].get("action", ""),
            "%s_attrs" % form_type: attrs.get("attrs", ""),
            "%s_class" % form_type: attrs["attrs"].get("class", ""),
            "%s_id" % form_type: attrs["attrs"].get("id", ""),
            "%s_method" % form_type: attrs.get("form_method", "post"),
            "%s_style" % form_type: attrs.get("form_style", None),
            "%s_tag" % form_type: attrs.get("form_tag", True),
            "disable_csrf": attrs.get("disable_csrf", False),
            "error_text_inline": attrs.get("error_text_inline", True),
            "field_class": attrs.get("field_class", ""),
            "field_template": attrs.get("field_template", ""),
            "flat_attrs": attrs.get("flat_attrs", ""),
            "form_error_title": attrs.get("form_error_title", None),
            "form_show_errors": attrs.get("form_show_errors", True),
            "form_show_labels": attrs.get("form_show_labels", True),
            "formset_error_title": attrs.get("formset_error_title", None),
            "help_text_inline": attrs.get("help_text_inline", False),
            "html5_required": attrs.get("html5_required", False),
            "include_media": attrs.get("include_media", True),
            "inputs": attrs.get("inputs", []),
            "is_formset": is_formset,
            "label_class": attrs.get("label_class", ""),
            "template_pack": self.template_pack,
        }

        # Handles custom attributes added to helpers
        for attribute_name, value in attrs.items():
            if attribute_name not in response_dict:
                response_dict[attribute_name] = value

        if "csrf_token" in context:
            response_dict["csrf_token"] = context["csrf_token"]

        return response_dict


@lru_cache()
def whole_uni_formset_template(template_pack=TEMPLATE_PACK):
    return get_template("%s/whole_uni_formset.html" % template_pack)


@lru_cache()
def whole_uni_form_template(template_pack=TEMPLATE_PACK):
    return get_template("%s/whole_uni_form.html" % template_pack)


class CrispyFormNode(BasicNode):
    def render(self, context):
        c = self.get_render(context).flatten()

        if self.actual_helper is not None and getattr(self.actual_helper, "template", False):
            template = get_template(self.actual_helper.template)
        else:
            if c["is_formset"]:
                template = whole_uni_formset_template(self.template_pack)
            else:
                template = whole_uni_form_template(self.template_pack)
        return template.render(c)


# {% crispy %} tag
@register.tag(name="crispy")
def do_uni_form(parser, token):
    """
    You need to pass in at least the form/formset object, and can also pass in the
    optional `crispy_forms.helpers.FormHelper` object.

    helper (optional): A `crispy_forms.helper.FormHelper` object.

    Usage::

        {% load crispy_tags %}
        {% crispy form form.helper %}

    You can also provide the template pack as the third argument::

        {% crispy form form.helper 'bootstrap' %}

    If the `FormHelper` attribute is named `helper` you can simply do::

        {% crispy form %}
        {% crispy form 'bootstrap' %}
    """
    token = token.split_contents()
    form = token.pop(1)

    helper = None
    template_pack = "'%s'" % get_template_pack()

    # {% crispy form helper %}
    try:
        helper = token.pop(1)
    except IndexError:
        pass

    # {% crispy form helper 'bootstrap' %}
    try:
        template_pack = token.pop(1)
    except IndexError:
        pass

    # {% crispy form 'bootstrap' %}
    if helper is not None and isinstance(helper, str) and ("'" in helper or '"' in helper):
        template_pack = helper
        helper = None

    if template_pack is not None:
        template_pack = template_pack[1:-1]
        ALLOWED_TEMPLATE_PACKS = getattr(
            settings, "CRISPY_ALLOWED_TEMPLATE_PACKS", ("bootstrap", "uni_form", "bootstrap3", "bootstrap4")
        )
        if template_pack not in ALLOWED_TEMPLATE_PACKS:
            raise template.TemplateSyntaxError(
                "crispy tag's template_pack argument should be in %s" % str(ALLOWED_TEMPLATE_PACKS)
            )

    return CrispyFormNode(form, helper, template_pack=template_pack)
