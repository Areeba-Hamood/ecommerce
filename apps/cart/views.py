from django.shortcuts import render,redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from apps.products.models import Products, ProductVariant
from .cart import Cart

# Create your views here.

@require_POST
def cart_add(request, product_id):
    cart = cart(request)
    product = get_object_or_404(Products, id=product_id, is_active=True)
    quantity = int(request.POST.get("quantity",1))
    variant_id = request.POST.get("variant_id")
    variant = None
    if variant_id:
        variant = get_object_or_404(ProductVariant, id=variant_id)
    cart.add(product, quantity, variant)
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"count": len(cart), 'subtotal': str(cart.subtotal)})
    return redirect("store:cart_detail")

def cart_detail(request):
    cart = Cart(request)
    return render(request, "cart/detail.html", {"cart":cart})

@require_POST
def cart_remove(request, item_key):
    Cart(request).remove(item_key)
    return redirect ("store:cart_detail")
