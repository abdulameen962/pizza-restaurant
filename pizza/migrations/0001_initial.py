# Generated by Django 4.2 on 2023-07-10 14:12

import cloudinary.models
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=5)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Creation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('slug', models.SlugField(blank=True, default=None, max_length=200, null=True)),
                ('description', models.TextField(max_length=500)),
                ('picture', cloudinary.models.CloudinaryField(blank=True, default=None, max_length=255, null=True, verbose_name='image')),
                ('price', models.FloatField(default=0)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('available', models.BooleanField(default=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='pizza_category', to='pizza.category')),
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
                ('picture', cloudinary.models.CloudinaryField(blank=True, default=None, max_length=255, null=True, verbose_name='image')),
                ('available', models.BooleanField(default=True)),
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
                ('picture', cloudinary.models.CloudinaryField(blank=True, default=None, max_length=255, null=True, verbose_name='image')),
                ('price', models.FloatField(default=0)),
                ('available', models.BooleanField(default=True)),
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
                ('profile_pic', cloudinary.models.CloudinaryField(blank=True, default=None, max_length=255, null=True, verbose_name='image')),
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
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('pieces', models.IntegerField()),
                ('price', models.FloatField()),
                ('order_date', models.DateTimeField(default=django.utils.timezone.now)),
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
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pizza_creation', to='pizza.pizza'),
        ),
        migrations.AddField(
            model_name='creation',
            name='toppings',
            field=models.ManyToManyField(blank=True, default=None, related_name='toppings_creation', to='pizza.topping'),
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('order_completed_date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('price', models.FloatField(default=0.0, verbose_name='Total price')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('items', models.ManyToManyField(blank=True, default=None, related_name='order_cart', to='pizza.order')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='user_cart', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Cart',
                'verbose_name_plural': 'Carts',
                'ordering': ('created_at',),
            },
        ),
    ]
