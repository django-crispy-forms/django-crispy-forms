from distutils import version

from django import get_version # TODO: remove when pre-CSRF token templatetags are no longer supported
from django.conf import settings
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
    warn("""You are using a version of Django that does not support the new csrf_token templatetag. It is advised that you upgrade to 1.1.2, 1.2, or another modern version of Django""")

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
    """ Some of our values need to be rendered safe as python variable names.
        So we just replaces hyphens with underscores.
    """
    return slugify(text).replace('-','_')


class BasicNode(template.Node):
    """ Basic Node object that we can rely on for Node objects in normal
        template tags. I created this because most of the tags we'll be using
        will need both the form object and the helper string. This handles
        both the form object and parses out the helper string into attributes
        that templates can easily handle."""

    def __init__(self, form, helper):
        self.form = template.Variable(form)
        self.helper = template.Variable(helper)

    def get_render(self, context):
        """ Render the Node """
        
        # TODO - rewrite cause this is dog-ugly.
        
        actual_form = self.form.resolve(context)
        helper = self.helper.resolve(context)
        attrs = None
        if helper:
            if not isinstance(helper, FormHelper):
                raise TypeError('helper object provided to uni_form tag must be a uni_form.helpers.FormHelper object.')
            attrs = helper.get_attr()
        form_class = ''
        form_id = ''
        form_method = 'post'
        form_action = ''
        form_tag = True
        inputs = []
        toggle_fields = set(())
        use_csrf_protection = True
        if attrs:
            form_tag = attrs.get("form_tag", True)
            form_method = attrs.get("form_method", form_method)
            form_action = attrs.get("form_action", form_action)
            form_class = attrs.get("class", '')
            form_id = attrs.get("id", "")
            inputs = attrs.get('inputs', [])
            toggle_fields = attrs.get('toggle_fields', set(()))
            use_csrf_protection = attrs.get('use_csrf_protection', True)
        final_toggle_fields = []
        if toggle_fields:
            final_toggle_fields = []
            for field in actual_form:
                if field.auto_id in toggle_fields:
                    final_toggle_fields.append(field)

        if helper and helper.layout:
            form_html = helper.render_layout(actual_form)
        else:
            form_html = ""
        response_dict = {
                        'form':actual_form,
                        'form_html':form_html,
                        'form_action':form_action,
                        'form_method':form_method,
                        'form_tag': form_tag,
                        'attrs':attrs,
                        'form_class' : form_class,
                        'form_id' : form_id,
                        'inputs' : inputs,
                        'toggle_fields': final_toggle_fields
                        }

        if not is_old_django: # TODO: remove when pre-CSRF token templatetags are no longer supported
            if use_csrf_protection and context.has_key('csrf_token'):
                response_dict['csrf_token'] = context['csrf_token']

        c = Context(response_dict)
        return c


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




