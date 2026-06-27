from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User


class UserRegisterForm(UserCreationForm): #UserCreationForm--->Instead of creating the registration form from scratch, Django provides UserCreationForm, which already includes:Password validation,Password confirmation,Password hashing,Security checks
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_number",
            "role",
            "password1",
            "password2",
        ]

class UserLoginForm(AuthenticationForm):
    pass