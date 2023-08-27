from datetime import date

from django import forms
from django.contrib.auth import get_user_model

from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForms(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput)

    class Meta:
        User = get_user_model()
        model = User
        fields = ["username", "first_name", "email"]

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Passwords don't match.")
        return cd["password2"]

    def clean_email(self):
        User = get_user_model()
        data = self.cleaned_data["email"]
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("Email already in use.")


class UserEditForm(forms.ModelForm):
    class Meta:
        User = get_user_model()
        model = User
        fields = ["first_name", "last_name", "email"]


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["date_of_birth", "photo"]

    def clean_date_of_birth(self):
        data = self.cleaned_data["date_of_birth"]
        if data > date.today():
            raise forms.ValidationError("Your date of birth cannot be in the future")
        return data
