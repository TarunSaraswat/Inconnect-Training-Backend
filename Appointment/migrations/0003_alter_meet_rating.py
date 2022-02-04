# Generated by Django 3.2.9 on 2022-02-03 08:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Appointment', '0002_auto_20220203_0806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meet',
            name='rating',
            field=models.IntegerField(default=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
