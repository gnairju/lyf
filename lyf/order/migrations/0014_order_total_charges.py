# Generated by Django 5.0 on 2024-01-06 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0013_order_del_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_charges',
            field=models.PositiveBigIntegerField(default=40),
        ),
    ]
