# Generated by Django 5.0 on 2024-02-07 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0032_order_invoice_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='invoice_id',
        ),
    ]
