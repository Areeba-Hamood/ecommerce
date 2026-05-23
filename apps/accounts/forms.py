from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Address

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    phone = forms.CharField(max_length=20, required=False)

    class Meta(UserCreationForm):
        model = User
        fields = ("username", "email", "first_name", "last_name", "phone", "password1", "password2")