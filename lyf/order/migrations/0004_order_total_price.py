# Generated by Django 5.0 on 2023-12-30 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_order_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]