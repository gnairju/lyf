# Generated by Django 5.0 on 2023-12-27 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_cart_price_alter_cart_days_needed_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='price',
        ),
    ]