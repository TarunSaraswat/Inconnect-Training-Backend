# Generated by Django 3.2.9 on 2022-02-03 07:02

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientMeet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booked', models.DateTimeField()),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('assigned_doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.doctors')),
                ('patient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.patients')),
            ],
        ),
    ]