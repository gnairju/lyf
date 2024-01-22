# Generated by Django 5.0 on 2024-01-22 17:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminPanel', '0023_product_address_product_availability_product_city_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offers',
            name='name',
        ),
        migrations.RemoveField(
            model_name='offers',
            name='offer_percentage',
        ),
        migrations.RemoveField(
            model_name='offers',
            name='offer_type',
        ),
        migrations.AddField(
            model_name='offers',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='adminPanel.categories'),
        ),
        migrations.AddField(
            model_name='offers',
            name='discount_percentage',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='offers',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='adminPanel.product'),
        ),
    ]
