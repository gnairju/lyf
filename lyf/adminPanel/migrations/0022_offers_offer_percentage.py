# Generated by Django 5.0 on 2024-01-16 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminPanel', '0021_offers'),
    ]

    operations = [
        migrations.AddField(
            model_name='offers',
            name='offer_percentage',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
