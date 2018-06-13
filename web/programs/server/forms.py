from django import forms


class SubmitForm(forms.Form):
    language = forms.CharField()
    content = forms.CharField()
    input = forms.CharField(required=False)
    username = forms.CharField()
