from django import forms


class TestForm(forms.Form):
    
    character_field = forms.CharField(label="Character Field", max_length=30, required=True, widget=forms.TextInput())    
    url_field = forms.URLField(label='URL field', verify_exists=False, max_length=100, required=True, widget=forms.TextInput())    
    textarea_field = forms.CharField(label='textarea_field'), required=True, widget=forms.Textarea())
