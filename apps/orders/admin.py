from django.contrib import admin
from .models import PaymentMethodConfig, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'product_variant', 'quantity', 'total')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user','status','payment_method','total','payment_status','created_at')
    list_filter = ('status', 'payment_status', 'payment_method','created_at')
    search_fields = ('order_number', 'shipping_name', 'shipping_phone_number', 'user__username')
    inlines = [OrderItemInline]
    readonly_fields=('order_number', 'total', 'subtotal','shipping_charges','discount', 'paid_at', 'created_at', 'updated_at')
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'notes', 'created_at', 'updated_at')
        }),
        ('pricing Snapshot', {
            'fields': ('subtotal', 'shipping_charges', 'discount', 'total')
        }),
        ('Shipping Address', {
            'fields': (
                'shipping_name', 'shipping_address_line_1', 'shipping_address_line_2',
                'shipping_city', 'shipping_state', 'shipping_zip_code', 'shipping_country',
                'shipping_phone_number', 'tracking_number'
            )
        }),
        ('Patment Details', {
            'fields': ('payment_method', 'payment_status', 'transaction_id', 'paid_at')
        }),
    )

@admin.register(PaymentMethodConfig)
class PaymentMethodConfigAdmin(admin.ModelAdmin):
    list_display = ('name','code','is_active','sandbox_mode')
    list_filter = ('is_active', 'sandbox_mode')
    search_fields = ('name', 'code')


# Register your models here.
