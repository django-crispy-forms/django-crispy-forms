# -*- coding: utf-8 -*-
from crispy_forms.bootstrap import Container
from crispy_forms.compatibility import integer_types, string_types
from crispy_forms.exceptions import DynamicError
from crispy_forms.layout import Fieldset, MultiField


class LayoutSlice(object):
    # List of layout objects that need args passed first before fields
    args_first = (Fieldset, MultiField, Container)

    def __init__(self, layout, key):
        self.layout = layout
        if isinstance(key, integer_types):
            self.slice = slice(key, key + 1, 1)
        else:
            self.slice = key

    def wrapped_object(self, LayoutClass, fields, *args, **kwargs):
        """
        Returns a layout object of type `LayoutClass` with `args` and `kwargs` that
        wraps `fields` inside.
        """
        if args:
            if isinstance(fields, list):
                fields = tuple(fields)
            else:
                fields = (fields,)

            if LayoutClass in self.args_first:
                arguments = args + fields
            else:
                arguments = fields + args

            return LayoutClass(*arguments, **kwargs)
        else:
            if isinstance(fields, list):
                return LayoutClass(*fields, **kwargs)
            else:
                return LayoutClass(fields, **kwargs)

    def pre_map(self, function):
        """
        Iterates over layout objects pointed in `self.slice` executing `function` on them.
        It passes `function` penultimate layout object and the position where to find last one
        """
        if isinstance(self.slice, slice):
            for i in range(*self.slice.indices(len(self.layout.fields))):
                function(self.layout, i)

        elif isinstance(self.slice, list):
            # A list of pointers  Ex: [[[0, 0], 'div'], [[0, 2, 3], 'field_name']]
            for pointer in self.slice:
                position = pointer[0]

                # If it's pointing first level
                if len(position) == 1:
                    function(self.layout, position[-1])
                else:
                    layout_object = self.layout.fields[position[0]]
                    for i in position[1:-1]:
                        layout_object = layout_object.fields[i]

                    try:
                        function(layout_object, position[-1])
                    except IndexError:
                        # We could avoid this exception, recalculating pointers.
                        # However this case is most of the time an undesired behavior
                        raise DynamicError("Trying to wrap a field within an already wrapped field, \
                            recheck your filter or layout")

    def wrap(self, LayoutClass, *args, **kwargs):
        """
        Wraps every layout object pointed in `self.slice` under a `LayoutClass` instance with
        `args` and `kwargs` passed.
        """
        def wrap_object(layout_object, j):
            layout_object.fields[j] = self.wrapped_object(
                LayoutClass, layout_object.fields[j], *args, **kwargs
            )

        self.pre_map(wrap_object)

    def wrap_once(self, LayoutClass, *args, **kwargs):
        """
        Wraps every layout object pointed in `self.slice` under a `LayoutClass` instance with
        `args` and `kwargs` passed, unless layout object's parent is already a subclass of
        `LayoutClass`.
        """
        def wrap_object_once(layout_object, j):
            if not isinstance(layout_object, LayoutClass):
                layout_object.fields[j] = self.wrapped_object(
                    LayoutClass, layout_object.fields[j], *args, **kwargs
                )

        self.pre_map(wrap_object_once)

    def wrap_together(self, LayoutClass, *args, **kwargs):
        """
        Wraps all layout objects pointed in `self.slice` together under a `LayoutClass`
        instance with `args` and `kwargs` passed.
        """
        if isinstance(self.slice, slice):
            # The start of the slice is replaced
            start = self.slice.start if self.slice.start is not None else 0
            self.layout.fields[start] = self.wrapped_object(
                LayoutClass, self.layout.fields[self.slice], *args, **kwargs
            )

            # The rest of places of the slice are removed, as they are included in the previous
            for i in reversed(range(*self.slice.indices(len(self.layout.fields)))):
                if i != start:
                    del self.layout.fields[i]

        elif isinstance(self.slice, list):
            raise DynamicError("wrap_together doesn't work with filter, only with [] operator")

    def map(self, function):
        """
        Iterates over layout objects pointed in `self.slice` executing `function` on them
        It passes `function` last layout object
        """
        if isinstance(self.slice, slice):
            for i in range(*self.slice.indices(len(self.layout.fields))):
                function(self.layout.fields[i])

        elif isinstance(self.slice, list):
            # A list of pointers  Ex: [[[0, 0], 'div'], [[0, 2, 3], 'field_name']]
            for pointer in self.slice:
                position = pointer[0]

                layout_object = self.layout.fields[position[0]]
                for i in position[1:]:
                    previous_layout_object = layout_object
                    layout_object = layout_object.fields[i]

                # If update_attrs is applied to a string, we call to its wrapping layout object
                if (
                    function.__name__ == 'update_attrs'
                    and isinstance(layout_object, string_types)
                ):
                    function(previous_layout_object)
                else:
                    function(layout_object)

    def update_attributes(self, **original_kwargs):
        """
        Updates attributes of every layout object pointed in `self.slice` using kwargs
        """
        def update_attrs(layout_object):
            kwargs = original_kwargs.copy()
            if hasattr(layout_object, 'attrs'):
                if 'css_class' in kwargs:
                    if 'class' in layout_object.attrs:
                        layout_object.attrs['class'] += " %s" % kwargs.pop('css_class')
                    else:
                        layout_object.attrs['class'] = kwargs.pop('css_class')
                layout_object.attrs.update(kwargs)

        self.map(update_attrs)
