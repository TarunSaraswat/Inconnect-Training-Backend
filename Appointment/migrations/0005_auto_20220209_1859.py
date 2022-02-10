# Generated by Django 3.2.9 on 2022-02-09 18:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Appointment', '0004_meet_done'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meet',
            old_name='booked',
            new_name='end_datetime',
        ),
        migrations.AddField(
            model_name='meet',
            name='start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 9, 18, 59, 38, 998633)),
            preserve_default=False,
        ),
    ]