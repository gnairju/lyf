# Generated by Django 5.0 on 2024-01-22 05:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_customuser_referral_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='referrer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='referred_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
