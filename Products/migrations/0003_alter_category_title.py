# Generated by Django 5.0.6 on 2024-07-06 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0002_product_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(choices=[('TShirt', 'TShirt'), ('Jeans', 'Jeans'), ('Jacket', 'Jacket'), ('Sweater', 'Sweater'), ('Shorts', 'Shorts'), ('Socks', 'Socks'), ('Shoes', 'Shoes')], max_length=255),
        ),
    ]
