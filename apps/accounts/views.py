from django.shortcuts import render , redirect
from django.contrib.auth import login , logout , authenticate
from django.contrib import messages
from .models import User
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.utils.encoding import force_bytes , force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm , SetPasswordForm
from .forms import UserRegistrationForm
from.forms import RegisterationForm, LoginForm, ProfileForm, AddressForm
from django.contrib.auth.decorators import login_required
from .models import Address
from orders.models import Order


# Create your views here.
def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful!")
            return redirect("accounts:login")
    else:
        form = UserRegistrationForm()
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
            messages.error(request,"Invalid username or password!")
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

def custom_forget_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        users = User.objects.filter(email=email)

        if users.exists():
            for user in users:
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_link = f"{request.scheme}://{request.get_host()}/auth/reset-confirm/{uid}/{token}"
                subject = "Reset your password"
                email_template = 'accounts/email/password_reset_email.html'
                parameters = {
                    "users":user,
                    "reset_link" : reset_link,
                }
                msg_html = render_to_string(email_template,parameters)
                
                send_mail(
                    subject,"Please reset your password by clicking on the link provided below",
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    html_message = msg_html,
                )
            messages.success(request, "Password reset link sent to your email")
            return redirect("accounts:login")
        else:
            messages.error(request, "No user found with this email address.")
    return render(request, 'accounts/forget_password.html')

def custom_password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            new_password =  request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Passwords reset successful")
                return redirect("login")
            else:
                messages.error(request, 'Password do not match!')
        return render(request, 'accounts/reset_password.html')
    else:
        return render(request, 'accounts/password_reset_invalid.html')

@login_required
def profile_view(request):
    form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile updated.")
        return redirect("profile")
    orders = Order.objects.filter(user=request.user).order_by("-created_at")[:10]
    return render(request,"accounts/profile.html",
                  {"form": form, "orders": orders})

@login_required
def address_list(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request,"accounts/addresses.html",{"addresses":addresses})  

@login_required
def address_create(request):
    form = AddressForm(request.POST or None)
    if form.is_valid():
        addr = form.save(commit=False)
        addr.user = request.user
        addr.save()
        messages.success(request, "Address saved.")
        return redirect("address_list")
    return render(request, "accounts/address_form.html",{"form":form})     


        




    


