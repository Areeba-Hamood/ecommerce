from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.utils import timezone
import random

from accounts.models import User, Address
from products.models import Products, Category, Wishlist, ProductVariant
from orders.models import Order, OrderItem, PaymentMethodConfig
from cart.cart import Cart

# Create your views here.

def home(request):
    featured_products = Products.objects.filter(is_active=True).prefetch_related('images')[:8]
    categories = Category.objects.filter(is_active=True)[:4]
    return render(request, "store/home.html",{
        "featured": featured_products,
        "categories": categories,
    })

@login_required
def wishlist_view(request):
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    products = wishlist.products.all()
    return render(request, "products/wishlist.html", {"products": products})

def wishlist_toggle(request,product_id):
    product = get_object_or_404(product, id=product_id, is_avaliable=True)
    wishlist, _= Wishlist.objects.get_or_create(user=request.user)

    if wishlist.Products.filter(id=product_id).exists():
        wishlist.Products.remove(product)
        added = False
        message = "Removed from your wishlist."
    else:
        wishlist.Products.add(product)
        added = True
        message = "Added to your wishlist."

