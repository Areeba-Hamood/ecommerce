from django.db import models
from accounts.models import User, Address
from products.models import ProductVariant, Products

# Create your models here.

class Order(models.Model):
    STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'confirmed'), 
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'), 
        ('cancelled', 'Cancelled'),
        ('refund', 'Refunded'),
    ]

    PAYMENT_METHOD = [
        ('cod','COD'),
        ('jazzcash','Jazzcash'),
        ('easypaisa','Easypaisa'),
        ('credit_card','Credit Card'),
        ('bank_transfer','Bank Transfer'),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name = 'orders')
    order_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=50 , choices=STATUS, default='pending')

    #pricing snapshot
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_charges = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    #address snapshot
    shipping_name =models.CharField(max_length=100)
    shipping_address_line_1 =models.CharField(max_length=100)
    shipping_address_line_2 =models.CharField(max_length=100)
    shipping_city =models.CharField(max_length=50)
    shipping_phone_number =models.CharField(max_length=15)

    #payment
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD, default='cod')
    payment_status = models.CharField(max_length=50, default='pending')
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    #shipping 
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    #timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    order= models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product= models.ForeignKey(Products, on_delete=models.SET_NULL, null=True, related_name='order_items')
    product_variant= models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True, related_name='order_items')
    quantity = models.IntegerField(default=1)
    total = models.DecimalField(max_digits=10, decimal_places=2)



