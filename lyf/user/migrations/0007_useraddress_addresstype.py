# Generated by Django 5.0 on 2023-12-27 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_useraddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraddress',
            name='addressType',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
    ]
