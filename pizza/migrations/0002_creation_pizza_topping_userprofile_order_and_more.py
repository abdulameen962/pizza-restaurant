# Generated by Django 4.2 on 2023-05-31 15:01

import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pizza', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Creation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField(max_length=500)),
                ('picture', cloudinary.models.CloudinaryField(blank=True, max_length=255, verbose_name='image')),
                ('price', models.FloatField(default=0)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Creation',
                'verbose_name_plural': 'Creations',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Pizza',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.FloatField(default=0)),
                ('picture', cloudinary.models.CloudinaryField(blank=True, max_length=255, verbose_name='image')),
            ],
            options={
                'verbose_name': 'Pizza',
                'verbose_name_plural': 'Pizza',
                'ordering': ('-name',),
            },
        ),
        migrations.CreateModel(
            name='Topping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('picture', cloudinary.models.CloudinaryField(blank=True, max_length=255, verbose_name='image')),
                ('price', models.FloatField(default=0)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ('-date_created',),
            },
        ),
        migrations.CreateModel(
            name='Userprofile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', cloudinary.models.CloudinaryField(blank=True, max_length=255, verbose_name='image')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User profile',
                'verbose_name_plural': 'Users profiles',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pieces', models.IntegerField()),
                ('price', models.FloatField()),
                ('order_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('order_completed_date', models.DateTimeField(blank=True)),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('COMPLETED', 'COMPLETED')], default='PENDING')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creation_orders', to='pizza.creation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='pizza.userprofile')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.AddField(
            model_name='creation',
            name='pizza',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pizza_creation', to='pizza.pizza'),
        ),
        migrations.AddField(
            model_name='creation',
            name='toppings',
            field=models.ManyToManyField(blank=True, related_name='toppings_creation', to='pizza.topping'),
        ),
    ]