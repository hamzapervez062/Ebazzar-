# Generated by Django 5.0.6 on 2024-08-03 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0005_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.IntegerField(blank=True, max_length=15, null=True),
        ),
    ]
