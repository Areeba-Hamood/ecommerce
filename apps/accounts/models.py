from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.TextField(unique = True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    
class Address(models.Model):
    ADDRESS_TYPES=(
        ('shipping', 'shipping'),
        ('billing', 'billing')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'addresses')
    address_type = models.CharField(max_length=10, choices = ADDRESS_TYPES)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)

    class Meta:
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return self.username
