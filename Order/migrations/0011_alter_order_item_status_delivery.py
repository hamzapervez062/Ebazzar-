# Generated by Django 5.0.6 on 2024-08-01 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0010_order_item_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_item',
            name='status_delivery',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Cancelled', 'Cancelled')], default='New', max_length=10),
        ),
    ]
