# Generated by Django 5.0 on 2024-01-21 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0026_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='distance',
            field=models.CharField(default=0, max_length=30),
        ),
    ]
