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

@login_required
def wishlist_toggle(request,product_id):
    product = get_object_or_404(Products, id=product_id, is_active=True)
    wishlist, _= Wishlist.objects.get_or_create(user=request.user)

    if wishlist.product.filter(id=product_id).exists():
        wishlist.product.remove(product)
        added = False
        message = "Removed from your wishlist."
    else:
        wishlist.product.add(product)
        added = True
        message = "Added to your wishlist."

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"added": added, "message": message})
    
    messages.success(request, message)
    return redirect(request.META.get('HTTP_REFERER', 'store:wishlist'))


def checkout_address(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, "your cart is empty.")
        return redirect("store:cart_detail")
    
    # if user is authenticated, check if they already have addresses
    addresses = []
    if request.user.is_authenticated:
        addresses = request.user.addresses.filter(address_type = 'shipping')

    if request.method == "POST":
        address_id = request.POST.get("saved_address")
        if address_id and request.user.is_authenticated:
            # user picked a saved address
            address = get_object_or_404(Address, id=address_id, user=request.user)
            request.session["checkout_address"] = {
                "first_name": address.first_name,
                "last_name": address.last_name,
                "address_line_1": address.address_line_1,
                "address_line_2": address.address_line_2,
                "city": address.city,
                "phone_number": address.phone_number,
                "country": "Pakistan",
            }
        else:
            # custom address inputs
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            address_line_1 = request.POST.get("address_line_1")
            address_line_2 = request.POST.get("address_line_2")
            city = request.POST.get("city")
            phone_number = request.POST.get("phone")
            save_address = request.POST.get("save_address")

            address_data = {
                "first_name": first_name,
                "last_name": last_name,
                "address_line_1": address_line_1,
                "address_line_2": address_line_2,
                "city": city,
                "phone_number": phone_number,
                "country": "pakistan",
            }

            request.session["checkout_address"] = address_data

            if save_address and request.user.is_authenticated:
                Address.objects.create(
                    user= request.user,
                    address_type= 'shipping',
                    first_name= first_name,
                    last_name= last_name,
                    address_line_1= address_line_1,
                    address_line_2= address_line_2,
                    city= city,
                    phone_number= phone_number,
                )

        return redirect("store:checkout_payment")
    
    return render(request, "store/checkout_address.html", {"addresses": addresses})

def checkout_payment(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect("store:cart_detail")
    if "checkout_address" not in request.session:
        messages.warning(request, "please enter shipping address first.")
        return redirect("store:checkout_address")
    
    # get active paymet method from DB( e.g COD, jazzcash, easypaisa)
    active_methods = PaymentMethodConfig.objects.filter(is_active=True)
    if not active_methods.exists():
        # fallback default COD method configration if DB is empty
        cod_config,_=PaymentMethodConfig.objects.get_or_create(
            code= "cod",
            defaults={"name": "Cash on Delivery", "is_active": True}
        )
        active_methods = [cod_config]

    if request.method == "POST":
        payment_code = request.POST.get("payment_method")
        
        # simulating payment details if it's JazzCash or EasyPaisa
        mobile_number = request.POST.get("mobile_number")
        pin = request.POST.get("wallet_pin")
        otp = request.POST.get("wallet_otp")

        selected_method = get_object_or_404(PaymentMethodConfig, code=payment_code,is_active=True)

        request.session["checkout_payment"] = {
            "code": selected_method.code,
            "name": selected_method.name,
            "mobile_number": mobile_number,
            "transaction_id": f"TXN-{random.randint(100000, 999999)}" if selected_method.code !="cod"
        }

        return redirect("store:checkout")
    
    return render(request, "store/checkout_payment.html", {"payment_methods": active_methods})

def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect("store:cart_detail")
    if "checkout_address" not in request.session:
        return redirect("store:checkout_address")
    if "checkout_payment" not in request.session:
        return redirect("store:checkout_payment")
    
    address = request.session["checkout_address"]
    payment = request.session["checkout_payment"]
    from decimal import Decimal
    shipping_charges = Decimal('299.00') #adding shipping charges
    subtotal = cart.subtotal
    total = subtotal + shipping_charges

    if request.method == "POST":
        try:
            with transaction.atomic():
                # generate unique order number
                order_num = f"LUX-{timezone.now().strftime('%y%m%d')}-{random.randint(1000, 9999)}"

                user = request.user if request.user.is_authenticated else None
                
                order = Order.objects.create(
                    user = user,
                    order_number = order_num,
                    status = "pending",
                    subtotal = subtotal,
                    shipping_charges = shipping_charges,
                    total = total,
                    shipping_name = f"{address['first_name']} {address['last_name']}",
                    shipping_address_line_1 = address['address_line_1'],
                    shipping_address_line_2 = address['address_line_2'],
                    shipping_city = address['city'],
                    shipping_country = address['country'],
                    shipping_phone_number = address['phone_number'],
                    payment_method = payment['code'],
                    payment_status = "paid" if payment['code'] != "cod" else "pending",
                    transaction_id = payment.get('transaction_id'),
                    paid_at = timezone.now() if payment['code'] != "cod" else None
                )

                for item in cart:
                    product = item['product']
                    variant = None
                    if item.get('variant_id'):
                        variant = ProductVariant.objects.get(id=item['variant_id'])
                        variant.stock_quantity -= item['quantity']
                        variant.save()
                    else:
                        Products.stock_quantity -= item['quantity']
                        Products.save()

                    OrderItem.objects.create(
                        order = order,
                        product = product,
                        product_variant = variant,
                        quantity = item['quantity'],
                        total = item['total'],
                    )

                # clear checkout session info and cart
                cart.clear()
                request.session["last_order_id"] = order.id
                del request.session["checkout_address"]
                del request.session["checkout_payment"]

                return redirect("store:checkout_success")
        except Exception as e:
            messages.error(request, f"An error occur while placing your order: {str(e)}")
            return redirect("store:checkout")

    return render(request, "store/checkout.html",{
        "cart": cart,
        "address": address,
        "payment": payment,
        "shipping_charges": shipping_charges,
        "total": total,
    })

def checkout_success(request):
    order_id = request.session.get("last_order_id")
    if not order_id:
        return redirect("store:home")
    
    order = get_object_or_404(Order, id= order_id)
    return render(request, "store/checkout_success.html", {"order": order})

def decimal_to_float(decimal_val):
    from decimal import Decimal
    if isinstance(decimal_val, Decimal):
        return float(decimal_val)
    return float(Decimal(str(decimal_val)))

    





