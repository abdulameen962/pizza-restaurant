# Generated by Django 4.2 on 2023-07-10 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.FloatField(default=0.0),
        ),
    ]
