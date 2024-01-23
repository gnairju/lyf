# Generated by Django 5.0 on 2024-01-22 19:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_customuser_referrer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(max_length=128, validators=[django.core.validators.MinLengthValidator(8), django.core.validators.MaxLengthValidator(128), django.core.validators.RegexValidator(code='invalid_password', message='Password must contain at least one number and one special character. It should be at least 8 characters long.', regex='^(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,}$')]),
        ),
    ]