from django import forms
from django.contrib.auth.models import User

from .models import Submission


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['content', 'input', 'language']


class RegistrationForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        label='',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        max_length=50,
        label='',
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Password'})
    )

    def clean(self):
        super().clean()
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            raise forms.ValidationError('This username is already taken.')


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        max_length=50,
        label='',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
