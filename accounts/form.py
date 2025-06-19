from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    full_name = forms.CharField(label="Full Name", max_length=100)
    email = forms.EmailField(label="Email")
    phone = forms.CharField(label="Phone Number", max_length=20)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")

        email = cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists.")

        return cleaned_data
    
class ResetPasswordForm(forms.Form):
    email = forms.EmailField(label="Email")
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm New Password")

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password")
        password2 = cleaned_data.get("confirm_password")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")

        return cleaned_data
