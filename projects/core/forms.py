from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model
from django.forms.widgets import PasswordInput, TextInput

User = get_user_model()


class CustomAuthenticationForm(auth_forms.AuthenticationForm):
    username = forms.CharField(widget=TextInput(
        attrs={'class': 'form-control validate', 'placeholder': 'Username', 'autocomplete': 'off'})
    )
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
