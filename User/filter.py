from django_filters.rest_framework import FilterSet
from User.models import Doctors, Patients


class PatientFilter(FilterSet):
    class Meta:
        model = Patients
        fields = {
            'name': ['exact']
        }


class DoctorFilter(FilterSet):
    class Meta:
        model = Doctors
        fields = {
            'name': ['exact']
        }
