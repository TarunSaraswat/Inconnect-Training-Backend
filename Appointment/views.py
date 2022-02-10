from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from Appointment.filters import MeetFilter
from User.models import Doctors, Patients
from Appointment.models import DoctorService, Meet
from Appointment.serializers import MeetSerializer


class AddRating(GenericAPIView, UpdateModelMixin):
    queryset = Meet.objects.all().filter(done=True)
    serializer_class = MeetSerializer
    permission_classes = [IsAuthenticated]


class MeetViewSet(viewsets.ModelViewSet):
    serializer_class = MeetSerializer
    permission_classes = [IsAuthenticated]
    queryset = Meet.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_class = MeetFilter

    def list(self, request, *args, **kwargs):
        obj = self.filter_queryset(self.get_queryset()).values_list('assigned_doctor', flat=True)
        doc = Doctors.objects.filter(id__in=obj).values_list('name')
        return Response(doc)

    def create(self, request, *args, **kwargs):
        serializer = MeetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        patient = Patients.objects.get(id=data.get('patient_id').id)
        doctor_at_zipcode = Doctors.objects.filter(zipcode=patient.zipcode).values_list('id', flat=True)
        doctor_service = DoctorService.objects.filter(service=data.get('service')).values_list('id', flat=True)
        doctor = [
            doctor_zipcode
            for doctor_zipcode in doctor_at_zipcode
            if doctor_zipcode in doctor_service
        ]
        assigned_doctor = None
        for d in doctor:
            booking_reject = False
            doc_meet = Meet.objects.filter(assigned_doctor=d)

            for meet in doc_meet:
                if meet.end_datetime < data.get('start_datetime'):
                    continue
                elif meet.start_datetime > data.get('end_datetime'):
                    continue
                else:
                    booking_reject = True
                    break
            if booking_reject:
                continue
            else:
                assigned_doctor = Doctors.objects.get(id=d)
                break
        if assigned_doctor:
            meet_serializer = Meet.objects.create(
                patient_id=patient, start_datetime=data.get('start_datetime'), end_datetime=data.get('end_datetime'),
                assigned_doctor=assigned_doctor, service=data.get('service'))
            meet_serializer.save()
            return Response(status=201)
        else:
            return Response(status=404, data={'issue': 'no free timeslot found for requested service'})


class GetByZipcode(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        zipcode = request.data.get('zipcode')
        doctors = Meet.objects.all().values_list('assigned_doctor', flat=True)
        doctors = list(set(doctors))
        doctors_list = Doctors.objects.filter(id__in=doctors, zipcode=zipcode).values_list('name')
        return Response(doctors_list)
