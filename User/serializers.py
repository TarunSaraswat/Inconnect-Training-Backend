from rest_framework import serializers
from User.models import Doctors, Patients


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctors
        fields = ['email', 'name', 'city', 'state', 'zipcode']


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patients
        fields = ['email', 'name', 'city', 'state', 'zipcode']
