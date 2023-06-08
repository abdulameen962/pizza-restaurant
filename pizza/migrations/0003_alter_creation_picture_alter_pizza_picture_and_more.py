# Generated by Django 4.2 on 2023-06-03 09:09

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pizza', '0002_creation_pizza_topping_userprofile_order_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creation',
            name='picture',
            field=cloudinary.models.CloudinaryField(blank=True, default=None, max_length=255, null=True, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='pizza',
            name='picture',
            field=cloudinary.models.CloudinaryField(blank=True, default=None, max_length=255, null=True, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='topping',
            name='picture',
            field=cloudinary.models.CloudinaryField(blank=True, default=None, max_length=255, null=True, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic',
            field=cloudinary.models.CloudinaryField(blank=True, default=None, max_length=255, null=True, verbose_name='image'),
        ),
    ]
