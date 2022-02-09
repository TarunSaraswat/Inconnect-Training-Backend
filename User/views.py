from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from User.filter import DoctorFilter, PatientFilter
from User.models import Doctors, Patients
from User.serializers import PatientSerializer, DoctorSerializer


class PatientViewSet(viewsets.ModelViewSet):
    """
    View set for patients
    """
    queryset = Patients.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filter_class = PatientFilter

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class DoctorViewSet(viewsets.ModelViewSet):
    """
    View set for Doctors
    """
    queryset = Doctors.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filter_class = DoctorFilter

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
