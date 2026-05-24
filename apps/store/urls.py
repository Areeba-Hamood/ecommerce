from . import views
from django.urls import path, include

app_name = 'store'

urlpatterns = [
    path('', views.home,    name='home'),
    path('about/', views.about,   name='about'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search,  name='search'),
    path('Products/', include('products.urls')),
    path('Cart/', include('cart.urls')),
    path('Orders/', include('orders.urls')),
]