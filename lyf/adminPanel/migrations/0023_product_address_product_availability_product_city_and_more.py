# Generated by Django 5.0 on 2024-01-20 04:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminPanel', '0022_offers_offer_percentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='address',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='availability',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='city',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator(code='invalid_phone_number', message='Phone number must contain only digits.', regex='^\\d{1,15}$')]),
        ),
        migrations.AddField(
            model_name='product',
            name='state',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='street',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]