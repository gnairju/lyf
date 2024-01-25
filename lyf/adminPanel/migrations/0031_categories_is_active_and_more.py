# Generated by Django 5.0 on 2024-01-25 06:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminPanel', '0030_alter_product_discounted_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='categoryoffer',
            name='discount_percentage',
            field=models.IntegerField(default=0, help_text='In Percentage', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)]),
        ),
    ]