from distutils import version

from django import get_version # TODO: remove when pre-CSRF token templatetags are no longer supported
from django.conf import settings
from django.forms.formsets import BaseFormSet
from django.template import Context, Template
from django.template.loader import get_template
from django import template

from django.template.defaultfilters import slugify

from uni_form.helpers import FormHelper

register = template.Library()

# csrf token fix hack. 
# TODO: remove when pre-CSRF token templatetags are no longer supported
django_version = get_version()
is_old_django = True
if version.LooseVersion(django_version) >= version.LooseVersion('1.1.2'):
    is_old_django = False
else:
    from warnings import warn
    warn("""You are using a version of Django that does not support the new csrf_token templatetag. 
        It is advised that you upgrade to 1.1.2, 1.2, or another modern version of Django""")

###################################################
# Core as_uni_form filter.
# You will likely use this simple filter
# most of the time.
# This is easy to get working and very simple in
# concept and execution.
###################################################
@register.filter
def as_uni_form(form):
    template = get_template('uni_form/uni_form.html')
    c = Context({'form':form})
    return template.render(c)

@register.filter
def as_uni_form_set(formset):
    template = get_template('uni_form/uni_form_set.html')
    c = Context({'formset':formset})
    return template.render(c)

@register.filter
def as_uni_errors(form):
    template = get_template('uni_form/errors.html')
    c = Context({'form':form})
    return template.render(c)

@register.filter
def as_uni_field(field):
    template = get_template('uni_form/field.html')
    c = Context({'field':field})
    return template.render(c)

@register.inclusion_tag("uni_form/includes.html", takes_context=True)
def uni_form_setup(context):
    """
    Creates the <style> and <script> tags needed to initialize the uni-form.

    Create a local uni-form/includes.html template if you want to customize how
    these files are loaded.
    """
    if 'MEDIA_URL' not in context:
        context['MEDIA_URL'] = settings.MEDIA_URL
    return (context)

############################################################################
#
# Everything from now on gets more fancy
# It can be argued that having django-uni-form construct your forms is overkill
# and that I am playing architecture astronaut games with form building.
#
# However, all the bits that follow are designed to be section 508 compliant,
# so all the fancy JS bits are garanteed to degrade gracefully.
#
############################################################################

def namify(text):
    """ 
    Some of our values need to be rendered safe as python variable names.
    So we just replaces hyphens with underscores.
    """
    return slugify(text).replace('-','_')


class BasicNode(template.Node):
    """ 
    Basic Node object that we can rely on for Node objects in normal
    template tags. I created this because most of the tags we'll be using
    will need both the form object and the helper string. This handles
    both the form object and parses out the helper string into attributes
    that templates can easily handle.
    """
    def __init__(self, form, helper):
        self.form = template.Variable(form)
        if helper is not None:
            self.helper = template.Variable(helper)
        else:
            self.helper = None

    def get_render(self, context):
        """ 
        Renders the Node.
        :param context: `django.template.Context` variable holding the context for the node

        Returns a `Context` object with all the necessary stuff to render the form.

        `self.form` and `self.helper` are resolved into real Python objects resolving them
        from the `context`. 
        The form can be a form or a formset:
            * If it's a form. If it's got a helper with a layout we use it, otherwise 
            `form_html` is not set and the template used for rendering the form will have 
            to use a default behavior. The form is stored in key `form`.
            * If it's a formset `is_formset` is set to True. The formset is stored in key
            `formset`.
        """
        actual_form = self.form.resolve(context)
        attrs = {}
        if self.helper is not None:
            helper = self.helper.resolve(context)

            if not isinstance(helper, FormHelper):
                raise TypeError('helper object provided to uni_form tag must be a uni_form.helpers.FormHelper object.')
            attrs = helper.get_attr()
        else:
            helper = None

        # We get the response dictionary 
        response_dict = self.get_response_dict(attrs, context)
        is_formset = isinstance(actual_form, BaseFormSet)

        # If we have a form and a layout we use it
        if helper and helper.layout and not is_formset:
            form_html = helper.render_layout(actual_form)
        else:
            form_html = ""

        if is_formset:
            response_dict.update({'formset': actual_form})
        else:
            response_dict.update({'form': actual_form})

        response_dict.update({
            'is_formset': is_formset,
            'form_html': form_html,
        })

        return Context(response_dict)

    def get_response_dict(self, attrs, context):
        """
        Returns a dictionary with all the parameters necessary to render the form in a template.
        
        :param attrs: Dictionary with the customized attributes of the form extracted from the helper
        :param context: `django.template.Context` for the node
        """
        # We take form parameters from attrs if they are set, otherwise we use defaults
        form_tag = attrs.get("form_tag", True)
        form_method = attrs.get("form_method", 'post')
        form_action = attrs.get("form_action", '.')
        form_class = attrs.get("class", '')
        form_id = attrs.get("id", "")
        inputs = attrs.get('inputs', [])
        toggle_fields = attrs.get('toggle_fields', set(()))
        use_csrf_protection = attrs.get('use_csrf_protection', True)

        final_toggle_fields = []
        if toggle_fields:
            for field in actual_form:
                if field.auto_id in toggle_fields:
                    final_toggle_fields.append(field)

        response_dict = {
            'form_action': form_action,
            'form_method': form_method,
            'form_tag': form_tag,
            'attrs': attrs,
            'form_class': form_class,
            'form_id': form_id,
            'inputs': inputs,
            'toggle_fields': final_toggle_fields,
        }

        # TODO: remove when pre-CSRF token templatetags are no longer supported
        if not is_old_django: 
            if use_csrf_protection and context.has_key('csrf_token'):
                response_dict['csrf_token'] = context['csrf_token']

        return response_dict

##################################################################
#
# Actual tags start here
#
##################################################################


@register.tag(name="uni_form")
def do_uni_form(parser, token):
    """
    You need to pass in at least the form object, and can also pass in the
    optional helper object. Writing the attrs string is rather challenging so
    use of the objects found in uni_form.helpers is encouraged.

    form: The forms object to be rendered by the tag

    helper (optional): A uni_form.helpers.FormHelper object.

    Example::

        {% uni_form my-form my_helper %}

    """
    token = token.split_contents()
    form = token.pop(1)

    try:
        helper = token.pop(1)
    except IndexError:
        helper = None

    return UniFormNode(form, helper)


class UniFormNode(BasicNode):
    def render(self, context):
        c = self.get_render(context)
        
        if c['is_formset']:
            template = get_template('uni_form/whole_uni_formset.html')
        else:
            template = get_template('uni_form/whole_uni_form.html')

        return template.render(c)


#################################
# uni_form scripts
#################################

@register.tag(name="uni_form_jquery")
def uni_form_jquery(parser, token):
    """
    toggle_field: For making fields designed to be toggled for editing add them
    by spaces. You must specify by field id (field.auto_id)::

        toggle_fields=<first_field>,<second_field>
    """
    token = token.split_contents()
    form = token.pop(1)
    
    try:
        attrs = token.pop(1)
    except IndexError:
        attrs = None

    return UniFormJqueryNode(form,attrs)


class UniFormJqueryNode(BasicNode):
    def render(self,context):
        c = self.get_render(context)
        template = get_template('uni_form/uni_form_jquery.html')

        return template.render(c)


# TODO: remove when pre-CSRF token templatetags are no longer supported
if is_old_django:
    # csrf token fix hack.     
    # Creates bogus csrf_token so we can continue to support older versions of Django.

    class CsrfTokenNode(template.Node):
        def render(self, context):
            return ''


    @register.tag(name="csrf_token")
    def dummy_csrf_token(parser, data):
        return CsrfTokenNode()




