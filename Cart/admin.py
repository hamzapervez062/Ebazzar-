from django.contrib import admin
from .models import Cart
# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_id', 'products', 'quantity', 'date_added', 'user', 'color', 'size']

admin.site.register(Cart, CartAdmin)
  