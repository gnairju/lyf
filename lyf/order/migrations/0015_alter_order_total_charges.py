# Generated by Django 5.0 on 2024-01-06 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0014_order_total_charges'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_charges',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]
