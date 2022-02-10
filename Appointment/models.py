from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from User.models import Patients, Doctors


class Meet(models.Model):
    patient_id = models.ForeignKey(Patients, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    assigned_doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=5)
    service = models.CharField(max_length=200)
    done = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.service


class DoctorService(models.Model):
    doctor_id = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    service = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.service
