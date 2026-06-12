from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Address

# Register your models here.
class AddressInline(admin.TabularInline):
    model = Address
    extra = 1

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone_number', 'first_name', 'last_name', 'is_staff')
    inlines = [AddressInline]
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Felds', {'fields': ('phone_number',)},),
    )

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address_type', 'first_name', 'last_name', 'city', 'phone_number')
    list_filter = ('address_type', 'city')
    search_fields = ('user__username', 'first_name', 'last_name', 'city')
    
