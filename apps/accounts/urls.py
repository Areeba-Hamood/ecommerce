from . import views
from django.urls import path

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forget-password/', views.custom_forget_password, name='forget-password'),
    path('reset-confirm/<str:uidb64>/<str:token>/', views.custom_password_reset_confirm, name='reset-confirm'),
]