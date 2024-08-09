# Generated by Django 5.0.6 on 2024-07-28 13:08

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_item',
            name='order_number',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
