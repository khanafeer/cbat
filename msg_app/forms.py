from django import forms
from django_password_strength.widgets import PasswordStrengthInput
class RegisterForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=PasswordStrengthInput())
    email = forms.EmailField()