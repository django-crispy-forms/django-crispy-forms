import re

from django.template import Library

register = Library()

default = {"base": "test default css", "text": "some text", "radioselect": "radio"}

default_radioselect = {
    "input": "test radio css",
}

checkbox = {
    "checkbox": "checkbox",
}


class CSSContainer:
    def __init__(self, css_styles):
        default_items = [
            "text",
            "number",
            "email",
            "url",
            "password",
            "hidden",
            "multiplehidden",
            "file",
            "clearablefile",
            "textarea",
            "date",
            "datetime",
            "time",
            "checkbox",
            "select",
            "nullbooleanselect",
            "selectmultiple",
            "radioselect",
            "checkboxselectmultiple",
            "multi",
            "splitdatetime",
            "splithiddendatetime",
            "selectdate",
        ]

        base = css_styles.get("base", "")
        for item in default_items:
            setattr(self, item, base)

        for key, value in css_styles.items():
            if key != "base":
                # get current attribute and rejoin with a set, also to ensure a space between each attribute
                current_class = set(getattr(self, key).split())
                current_class.update(set(value.split()))
                new_classes = " ".join(current_class)
                setattr(self, key, new_classes)

    def __repr__(self):
        return str(self.__dict__)

    def __add__(self, other):
        for field, css_class in other.items():
            current_class = set(getattr(self, field).split())
            current_class.update(set(css_class.split()))
            new_classes = " ".join(current_class)
            setattr(self, field, new_classes)
        return self

    def __sub__(self, other):
        for field, css_class in other.items():
            current_class = set(getattr(self, field).split())
            removed_classes = set(css_class.split())
            new_classes = " ".join(current_class - removed_classes)
            setattr(self, field, new_classes)
        return self

    def get_input_class(self, field):
        widget_name = re.sub(r"widget$|input$", "", field.field.widget.__class__.__name__.lower())
        return getattr(self, widget_name)
