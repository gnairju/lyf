# Generated by Django 5.0 on 2024-01-07 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminPanel', '0014_coupons_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupons',
            name='coupon_type',
            field=models.CharField(blank=True, choices=[('delivery', 'delivery'), ('caution', 'caution'), ('Total', 'Total')], max_length=30),
        ),
    ]
