from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Address

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    phone = forms.CharField(max_length=20, required=False)

    class Meta(UserCreationForm):
        model = User
        fields = ("username", "email", "first_name", "last_name", "phone", "password1", "password2")

class CustomUserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=20, required=false)

    class Meta:
        model = User
        fields = ("username","email","first_name","last_name","phone",
                 "password1","password2")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.")
        return email

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")

class profileForm(forms.ModelsForm):
    class Meta:
        model = User
        fields = ("first_name","last_name","phone")
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude= ("user",)



