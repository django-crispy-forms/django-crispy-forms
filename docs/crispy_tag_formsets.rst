==============================
{% crispy %} tag with formsets
==============================

``{% crispy %}`` tag supports formsets rendering too, all kind of Django formsets: formsets, modelformsets and inline formsets. In this section, it's taken for granted that you are familiar with previous explained crispy-forms concepts in the docs, like ``FormHelper``, how to set ``FormHelper`` attributes or render a simple form using ``{% crispy %}`` tag.


Formsets
~~~~~~~~

It's not the purpose of this documentation to explain how formsets work in detail, for that you should check `Django official formset docs`_. Let's start creating a formset using the previous ``ExampleForm`` form::

    from django.forms.models import formset_factory

    ExampleFormSet = formset_factory(ExampleForm, extra=3)
    formset = ExampleFormSet()

This is how you would render the formset using default rendering, no layouts or form helpers::

    {% crispy formset %}

Of course, you can still use a helper, otherwise there would be nothing crispy in this. When using a ``FormHelper`` with a formset compared to when you use it with a form, the main difference is that helper attributes are applied to the form structure, while the layout is applied to the formset’s forms. Let's create a helper for our ``ExampleFormSet``::

    class ExampleFormSetHelper(FormHelper):
        def __init__(self, *args, **kwargs):
            super(ExampleFormSetHelper, self).__init__(*args, **kwargs)
            self.form_method = 'post'
            self.layout = Layout(
                'favorite_color',
                'favorite_food',
            )
            self.render_required_fields = True

This helper is quite easy to follow. We want our form to use ``POST`` method, and we want ``favorite_color`` to be the first field, then ``favorite_food`` and finally we tell crispy to render all required fields after. Let's go and use it, when using ``{% crispy %}`` tag in a template there is one main difference when rendering formsets vs forms, in this case you need to specify the helper explicitly.

This would be part of an hypothetic function view::

    formset = ExampleFormSet()
    helper = ExampleFormSetHelper()
    return render(request, 'template.html', {'formset': formset, 'helper': helper})

Then in **template.html** you would have to do::

    {% crispy formset helper %}

There are two ways you can add submit buttons to a formset. Using ``FormHelper.add_input`` method::

    helper.add_input(Submit("submit", "Save"))

Or you can set ``FormHelper.form_tag`` to ``False`` and control the formset outer structure at your will writing boring HTML::

    <form action="{% url 'save_formset' %}" method="POST">
        {% crispy formset helper %}
        <div class="form-actions">
            <input type="submit" name="submit" value="Save" class="btn btn-primary" id="submit-save">
        </div>
    </form>

Finally, model formsets and inline formsets are rendered exactly the same as formsets, the only difference is how you build them in your Django code.

.. _`Django official formset docs`: https://docs.djangoproject.com/en/dev/topics/forms/formsets/

Extra context
~~~~~~~~~~~~~

Rendering any kind of formset with crispy injects some extra context in the layout rendering so that you can do things like::

    HTML("{% if forloop.first %}Message displayed only in the first form of a formset forms list{% endif %}",
    Fieldset("Item {{ forloop.counter }}", 'field-1', [...])

Basically you can access a ``forloop`` Django node, as if you were rendering your formsets forms using a for loop.


Custom templates and table inline formsets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default formset template will render your formset's form using divs, but many times people prefer tables for formsets. Don't worry, crispy-forms's got you covered. ``FormHelper`` has an attribute named ``template`` that can be used to specify a custom template for rendering a form or formset, in this case a formset. Obviously when we specify a ``template`` attribute, we are making that helper only usable with forms or formsets.

The name of the template to use is **table_inline_formset.html** and you use it doing::

    helper.template = 'bootstrap/table_inline_formset.html'

The best part is that if this template doesn't do exactly what you want, you can copy it into your templates folder, customize it and then link your helper to your alternative version. If you think what you are missing would be valuable to others, then please submit a pull request at github.

.. warning ::

    This template doesn't currently take into account any layout you have specified and only works with bootstrap template pack.


Formset forms with different layouts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default crispy-forms formset rendering shares the same layout among all formset's forms. This is the case 99% of the times. But maybe you want to render your formset's forms using different layouts that you cannot achieve using the extra context injected, for that you will have to create and use a custom template. Most likely you will want to do::

    {{ formset.management_form|crispy }}
    {% for form in formset %}
        {% crispy form %}
    {% endfor %}

Where every ``form`` has a ``helper`` attribute from which crispy will grab the layout. In your view you will need to change the layout or use a different help for every formset's form. Make sure that you have ``form_tag`` attribute set to ``False``, otherwise you will get 3 individual forms rendered.
