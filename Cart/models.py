from django.db import models
from Products.models import Product
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.

class Cart(models.Model):   
    cart_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField() 
    color = models.CharField(max_length=255)
    size = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)

    def sub_total(self):
        return self.products.price * self.quantity

    
    
    
    
    @property
    def product_id(self):
        return self.Product.pk
    
    
    
