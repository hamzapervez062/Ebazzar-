# from Order.models import Shippinginfo, Paymentinfo, Order_item
# from Cart.models import Cart
# from django.db.models.signals import post_delete, pre_delete, post_save, pre_save
# from django.dispatch import receiver
# import uuid
# from django.contrib.auth.models import User
# from django.db import transaction


# Signal handler for post_delete on Cart@receiver(pre_delete, sender=Cart)
# @receiver(pre_delete, sender=Cart)
# def update_order_item_on_cart_delete(sender, instance, **kwargs):
#     updated_count = Order_item.objects.filter(cart=instance).update(cart=instance)
#     updated_count.save()

#     print(f"deleted {instance} {updated_count}")	
