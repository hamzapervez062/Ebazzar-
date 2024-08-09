from django.contrib import admin
from .models import Order_item, Paymentinfo, Shippinginfo
# Register your models here.
@admin.register(Order_item)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number','product_id', 'item' , 'user', 'cart', 'shipping', 'status_delivery', 'order_total', 'tax', 'sub_total' ,'delivery_charges', 'payment', 'quantity', 'product_price', 'created_at']

@admin.register(Paymentinfo)
class PaymentinfoAdmin(admin.ModelAdmin):
    list_display = ['payment_id','user',  'payment_method', 'amount_paid', 'status', 'created_at']

@admin.register(Shippinginfo)
class ShippinginfoAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'country', 'state', 'city', 'order_note']
