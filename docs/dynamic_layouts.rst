==========================
Updating layouts on the go
==========================

Layouts can be changed, adapted and generated programmatically.

The next sections will explain how to select parts of a layout and update them. We will use this API from the ``FormHelper`` instance and not the layout itself. This API's basic behavior consists of selecting the piece of the layout to manipulate and chaining methods that alter it after that.

Selecting layout objects with slices
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can get a slice of a layout using familiar ``[]`` Python operator::

    form.helper[1:3]
    form.helper[2]
    form.helper[:-1]

You can basically do all kind of slices, the same ones supported by Python's lists. You can also concatenate them. If you had this layout::

    Layout(
        Div('email')
    )

You could access ``'email'`` string doing::

    form.helper[0][0]

wrap
~~~~

One useful action you can apply on a slice is ``wrap``, which wraps every selected field using a layout object type and parameters passed. Let's see an example. If We had this layout::

    Layout(
       'field_1',
       'field_2',
       'field_3'
    )

We could do::

    form.helper[1:3].wrap(Field, css_class="hello")

We would en up having this layout::

    Layout(
       'field_1',
       Field('field_2', css_class='hello'),
       Field('field_3', css_class='hello')
    )

Note how ``wrap`` affects every different layout object selected, if you would like to wrap ``field_2`` and ``field_3`` together in a ``Field`` layout object you will have to use ``wrap_together``.

Beware that the slice ``[1:3]`` only looks in the first level of depth of the layout. So if the previous layout was this way::

    Layout(
       'field_1',
       Div('field_2'),
       'field_3'
    )

``helper[1:3]`` would return this layout::

    Layout(
       'field_1',
       Field(Div('field_2'), css_class="hello"),
       Field('field_3', css_class="hello")
    )

all
~~~

This method selects all first level of depth layout objects::

    form.helper.all().wrap(Field, css_class="hello")

Selecting a field name
~~~~~~~~~~~~~~~~~~~~~~

If you pass a string with the field name, this field name will be searched greedy throughout the whole Layout depth levels. Imagine we have this layout::

    Layout(
       'field_1',
       Div(
           Div('password')
        ),
       'field_3'
    )

If we do::

    form.helper['password'].wrap(Field, css_class="hero")

Previous layout would become::

    Layout(
       'field_1',
       Div(
           Div(
               Field('password', css_class="hero")
           )
        ),
       'field_3'
    )

filter
~~~~~~

This method will allow you to filter layout objects by its class type, applying actions to them::

    form.helper.filter(basestring).wrap(Field, css_class="hello")
    form.helper.filter(Div).wrap(Field, css_class="hello")

Filter is not greedy, so it only searches first depth level.

FormHelper with a form attached
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Since version 1.2.0 ``FormHelper`` optinally can be passed an instance of a form. You would do it this way::

    class ExampleForm(forms.Form):
        def __init__(self, *args, **kwargs):
            super(ExampleForm, self).__init__(*args, **kwargs)
            self.helper = FormHelper(self)

That makes the helper able to cross match the layout with the form instance, being able to search by widget type. Also when you do this django-crispy-forms builds a default layout using ``form.fields`` for you, so you don't have to manually list them all if your form is huge.

filter_by_widget
~~~~~~~~~~~~~~~~

This method assumes you are using a helper with a form attached, you could filter by widget type doing::

    form.helper.filter_by_widget(forms.PasswordInput).wrap(Field, css_class="hero")

``filter_by_widget`` is greedy by default, so it searches in depth. Let's see a use case exmpale, imagine we have this Layout::

    Layout(
       'username',
       Div('password1'),
       Div('password2')
    )

Supposing ``password1`` and ``password2`` fields are using widget ``PasswordInput``, would turn into::

    Layout(
       'username',
       Div(Field('password1', css_class="hero")),
       Div(Field('password2', css_class="hero"))
    )

An interesting real use case example here would be to wrap all ``SelectInputs`` with a custom made ``ChosenField`` that renders the field using a chosenjs compatible field.

Manipulating a layout
~~~~~~~~~~~~~~~~~~~~~

Besides selecting layout objects and applying actions to them, you can also manipulate layouts themselves and layout obejcts easily, like if they were lists. We won't do this from the helper, but the layout and layout objects themselves. Consider this a lower level API.

All layout objects that can wrap others, contain a inner attribute ``fields`` which is a list, not a dictionary as in Django forms. You can apply any list methods on them easily. Beware that a ``Layout`` behaves itself like other layout objects such as ``Div``, the only difference is that it is the root of the tree.

This is how you would replace a layout object for other::

    layout[0][3][1] = Div('field_1')

This is how you would add one layout object at the end of the Layout::

    layout.append(HTML("<p>whatever</p>"))

This is how you would add one layout object at the end of another layout object::

    layout[0].append(HTML("<p>whatever</p>"))

This is how you would add several layout objects to a Layout::

    layout.extend([
        HTML("<p>whatever</p>"),
        Div('add_field_on_the_go')
    ])

This is how you would add several layout objects to another layout object::

    layout[0][2].extend([
        HTML("<p>whatever</p>"),
        Div('add_field_on_the_go')
    ])

This is how you would delete the second layout object within the Layout::

    layout.pop(1)

This is how you wold delete the second layout object within the second layout object::

    layout[1].pop(1)

This is how you would insert a layout object in the second position of a Layout::

    layout.insert(1, HTML("<p>whatever</p>"))

This is how you would insert a layout object in the second position of the second layout object::

    layout[1].insert(1, HTML("<p>whatever</p>"))


.. Warning ::

    Remember always that if you are going to manipulate a helper or layout in a view or any part of your code, you better use an instance level variable.
