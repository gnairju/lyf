# Generated by Django 5.0 on 2024-01-07 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminPanel', '0016_alter_coupons_discount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coupons',
            old_name='number',
            new_name='num',
        ),
    ]
