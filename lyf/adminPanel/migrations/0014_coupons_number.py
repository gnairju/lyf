# Generated by Django 5.0 on 2024-01-07 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminPanel', '0013_coupons_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupons',
            name='number',
            field=models.BigIntegerField(default=25),
        ),
    ]
