from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
from Cart.models import Cart
from Products.models import Product
import uuid

# Create your models here.
class Paymentinfo(models.Model):
    payment_status = (
        ('Pending', 'Pending'),
        ('Cancelled', 'Cancelled'),
        ('Refunded', 'Refunded'),
        ('Completed', 'Completed'),
        ('Processing', 'Processing'),

    )
    payment_me = (
        ('Cash On Delivery', 'Cash On Delivery'),
        ('Paypal', 'Paypal'),
    )
    payment_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100, choices=payment_me)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=100, choices=payment_status, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

class Shippinginfo(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    order_note = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Order_item(models.Model):
    STATUS = (
        ('Accepted', 'Accepted'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, related_name='order_items', on_delete=models.SET_NULL, null=True)
    shipping = models.ForeignKey(Shippinginfo, related_name='orders', on_delete=models.CASCADE)
    payment = models.ForeignKey(Paymentinfo, related_name='order', on_delete=models.CASCADE)
    status_delivery = models.CharField(max_length=10, choices=STATUS, default='New')
    order_total = models.FloatField()
    tax = models.FloatField()
    sub_total = models.FloatField()
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_id = models.IntegerField()
    order_number = models.IntegerField()
    delivery_charges = models.FloatField(blank=True, null=True)
    quantity = models.IntegerField(default=1)
    product_price = models.DecimalField(max_digits=10, decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)

    
    
    def get_absolute_url(self):
        return f'/ordercomplete/{self.order_number}/'
    
    def sub_ttotal(self):
        return self.sub_total

    

