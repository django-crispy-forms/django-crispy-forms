from django import forms
from django.db import models

from crispy_forms.helper import FormHelper


class SampleForm(forms.Form):
    is_company = forms.CharField(label="company", required=False, widget=forms.CheckboxInput())
    email = forms.EmailField(
        label="email", max_length=30, required=True, widget=forms.TextInput(), help_text="Insert your email"
    )
    password1 = forms.CharField(label="password", max_length=30, required=True, widget=forms.PasswordInput())
    password2 = forms.CharField(label="re-enter password", max_length=30, required=True, widget=forms.PasswordInput())
    first_name = forms.CharField(label="first name", max_length=5, required=True, widget=forms.TextInput())
    last_name = forms.CharField(label="last name", max_length=5, required=True, widget=forms.TextInput())
    datetime_field = forms.SplitDateTimeField(label="date time", widget=forms.SplitDateTimeWidget())

    def clean(self):
        super().clean()
        password1 = self.cleaned_data.get("password1", None)
        password2 = self.cleaned_data.get("password2", None)
        if not password1 and not password2 or password1 != password2:
            raise forms.ValidationError("Passwords dont match")

        return self.cleaned_data


class SampleForm2(SampleForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)


class CheckboxesSampleForm(forms.Form):
    checkboxes = forms.MultipleChoiceField(
        choices=((1, "Option one"), (2, "Option two"), (3, "Option three")),
        initial=(1,),
        widget=forms.CheckboxSelectMultiple,
    )

    alphacheckboxes = forms.MultipleChoiceField(
        choices=(("option_one", "Option one"), ("option_two", "Option two"), ("option_three", "Option three")),
        initial=("option_two", "option_three"),
        widget=forms.CheckboxSelectMultiple,
    )

    numeric_multiple_checkboxes = forms.MultipleChoiceField(
        choices=((1, "Option one"), (2, "Option two"), (3, "Option three")),
        initial=(1, 2),
        widget=forms.CheckboxSelectMultiple,
    )

    inline_radios = forms.ChoiceField(
        choices=(("option_one", "Option one"), ("option_two", "Option two"),),
        widget=forms.RadioSelect,
        initial="option_two",
    )


class CrispyTestModel(models.Model):
    email = models.CharField(max_length=20)
    password = models.CharField(max_length=20)


class SampleForm3(forms.ModelForm):
    class Meta:
        model = CrispyTestModel
        fields = ["email", "password"]
        exclude = ["password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)


class SampleForm4(forms.ModelForm):
    class Meta:
        """
        before Django1.6, one cannot use __all__ shortcut for fields
        without getting the following error:
        django.core.exceptions.FieldError: Unknown field(s) (a, l, _) specified for CrispyTestModel
        because obviously it casts the string to a set
        """

        model = CrispyTestModel
        fields = "__all__"  # eliminate RemovedInDjango18Warning


class SampleForm5(forms.Form):
    choices = [
        (1, 1),
        (2, 2),
        (1000, 1000),
    ]
    checkbox_select_multiple = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=choices)
    radio_select = forms.ChoiceField(widget=forms.RadioSelect, choices=choices)
    pk = forms.IntegerField()


class SampleFormWithMedia(forms.Form):
    class Media:
        css = {"all": ("test.css",)}
        js = ("test.js",)


class SampleFormWithMultiValueField(forms.Form):
    multi = forms.SplitDateTimeField()


class CrispyEmptyChoiceTestModel(models.Model):
    fruit = models.CharField(choices=[("apple", "Apple"), ("pear", "Pear")], null=True, blank=True,)


class SampleForm6(forms.ModelForm):
    class Meta:
        """
        When allowing null=True in a model field,
        the corresponding field will have a choice
        for the empty value.

        When the form is initialized by an instance
        with initial value None, this choice should
        be selected.
        """

        model = CrispyEmptyChoiceTestModel
        fields = ["fruit"]
        widgets = {"fruit": forms.RadioSelect()}


class SampleForm7(forms.ModelForm):
    is_company = forms.CharField(label="company", required=False, widget=forms.CheckboxInput())
    password2 = forms.CharField(label="re-enter password", max_length=30, required=True, widget=forms.PasswordInput())

    class Meta:
        model = CrispyTestModel
        fields = ("email", "password", "password2")


class SampleForm8(forms.ModelForm):
    is_company = forms.CharField(label="company", required=False, widget=forms.CheckboxInput())
    password2 = forms.CharField(label="re-enter password", max_length=30, required=True, widget=forms.PasswordInput())

    class Meta:
        model = CrispyTestModel
        fields = ("email", "password2", "password")
