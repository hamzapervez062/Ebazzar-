# Generated by Django 5.0.6 on 2024-07-28 17:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cart', '0004_alter_cart_color_alter_cart_size'),
        ('Order', '0003_alter_order_item_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_item',
            name='cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_items', to='Cart.cart'),
        ),
    ]
