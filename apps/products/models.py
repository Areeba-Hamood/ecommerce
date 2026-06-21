from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)
    #parent = models.ForeignKey('self', on_delete = models.CASCADE, related_name = 'children')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

class Products(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    #sku = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name = 'products')
    #image = models.ImageField(upload_to='product_images/')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    is_avaliable = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ProductsImage(models.Model):
    products = models.ForeignKey(Products, on_delete=models.CASCADE, related_name ='images')
    image = models.ImageField(upload_to='product_images/')
    alt_text = models.CharField(max_length=200)
    is_primary_image = models.BooleanField(default = False)
    order = models.PositiveIntegerField(default=0)

class ProductVariant(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name = 'variants')
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)
    stock_quantity = models.IntegerField(default=0)

class Whishlist(model.Models):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="whishlist")
    products = models.ManyToManyField(Product, related_name="whishlists", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def__str__(self):
        return f"Whishlist of {self.user.username}"