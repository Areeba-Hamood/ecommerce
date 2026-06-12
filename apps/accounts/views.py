from django.shortcuts import render, request, redirect
from django.contrib import messages
from django.contrib.auth import login , logout , authenticate
from .forms import UserRegistrationForm
from.forms import RegisterForm, LoginForm, ProfileForm, AddressForm
from django.contrib.auth.decorators import login_required
from .models import Address
from orders.models import Order
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your views here.
def register_view(request):
    if request.user.is_authenticated:
        return redirect("store:home")
    form = UserRegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request,user)
        messages.success(request, "Registration successful!")
        return redirect("store:home")    

    return render(request, 'accounts/register.html', {'form':form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("store:home")
    form = LoginForm(request,request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request,user)
        next_url = request.GET.get("next", "store:home")
        return redirect(next_url)
        
    return render(request, 'accounts/login.html', {"form": form})


def logout_view(request):
    logout(request)
    return redirect("store:home")


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


        




    


