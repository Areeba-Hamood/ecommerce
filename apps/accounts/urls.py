from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('forget-password/', views.custom_forget_password, name='forget-password'),
    path('reset-confirm/<str:uidb64>/<str:token>/', views.custom_password_reset_confirm, name='reset-confirm'),
]