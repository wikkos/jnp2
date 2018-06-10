from django import forms


class SendCodeForm(forms.Form):
    code = forms.CharField()
    input = forms.CharField()