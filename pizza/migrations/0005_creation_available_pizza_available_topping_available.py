# Generated by Django 4.2 on 2023-06-11 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza', '0004_category_creation_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='creation',
            name='available',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='pizza',
            name='available',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='topping',
            name='available',
            field=models.BooleanField(default=True),
        ),
    ]
