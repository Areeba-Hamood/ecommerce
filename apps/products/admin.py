from django.contrib import admin
from .models import Product, Category, ProductImage, ProductVariant, Whishlist


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    prepopulated_fields ={'slug':('name')}

@admin.Register

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'discounted_price', 'stock_quantity', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'category_name', 'description')
    inlines = [ProductImageInline, ProductVariantInline]
    prepopulated_fields = {'slug':('name')}


# Register your models here.
