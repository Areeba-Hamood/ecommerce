from django.urls import path, include
from . import views
from django.views.generic import RedirectView
import products.views as products_views
import cart.views as cart_views

app_name = 'store'

urlpatterns = [
    path("", views.home, name = 'home'),
    path("products/", products_views.product_list, name = 'product_list'),
    path("products/<slug:slug>", products_views.product_detail, name = 'product_detail'),
   
    #cart
    path('cart/', cart_views.cart_detail, name ='cart_detail'),
    path('cart/add/<int:product_id>', cart_views.cart_add, name ='cart_add'),
    path('cart/remove/<str:item_key>', cart_views.cart_remove, name ='cart_remove'),
   
    #wishlist
    path('wishlist/', views.wishlist_view, name ='wishlist'),
    path('wishlist/toggle/<int:product_id>/', views.wishlist_toggle, name ='wishlist_toggle'),
   
    #checkout
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/address/', views.checkout_address, name='checkout_address'),
    path('checkout/payment/', views.checkout_payment, name='checkout_payment'),
    path('checkout/success/', views.checkout_success, name='checkout_success'),    

]