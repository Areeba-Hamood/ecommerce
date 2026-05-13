from django.shortcuts import render , redirect
from django.contrib.auth import login , logout
from django.contrib.auth import messages
from .model import CustomUser
from django utlis.http import urlsafe_base64_encode , urlsafe_base64_decode
from django utlis.encoding import force_bytes , force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm , SetPasswordForm
from .form import CustomUserRegistrationForm


# Create your views here.
def register_view(request):
    if request.method == "POST":
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful!")
            return redirect("login")
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'accounts/register.html', {'form':form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            message.error(request,"Invalid username or password!")
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

def custom_forget_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        users = CustomUser.objects.filter(email=email)

        if users.exists():
            for user in users:
            uid = urlsafe_base64_encode(force_bytes{user.pk})
            token = default_token_generator.make_token(user)

            #url construction



    


