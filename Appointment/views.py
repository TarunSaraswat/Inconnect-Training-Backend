from datetime import datetime
from Appointment.filters import MeetFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from Appointment.filters import MeetFilter
from User.models import Doctors, Patients
from .models import DoctorService, Meet
from .serializers import MeetSerializer


class AddRating(GenericAPIView, UpdateModelMixin):
    queryset = Meet.objects.all().filter(done=True)
    serializer_class = MeetSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


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
        data = MeetSerializer(data=request.data)
        if data.is_valid():
            start_datetime = data['start_datetime'].value
            end_datetime = data['end_datetime'].value
            start_datetime = datetime.strptime(start_datetime, "%Y-%m-%dt%H:%M:%S")
            end_datetime = datetime.strptime(end_datetime, "%Y-%m-%dt%H:%M:%S")
            if start_datetime > end_datetime:
                return Response(status=400)
            patient_id = data['patient_id'].value
            service = data['service'].value
            patient = Patients.objects.get(id=patient_id)
            doctor_at_zipcode = Doctors.objects.filter(zipcode=patient.zipcode).values_list('id', flat=True)
            doctor_service = DoctorService.objects.filter(service=service).values_list('id', flat=True)
            doctor = []
            for docZipcode in doctor_at_zipcode:
                print(docZipcode)
                for docService in doctor_service:
                    print(docService)
                    if docZipcode == docService:
                        doctor.append(docZipcode)
            if not doctor:
                return Response(status=404)

            bookings = []
            for d in doctor:
                booking_reject = False
                doc_meet = Meet.objects.filter(assigned_doctor=d)

                for meet in doc_meet:
                    if meet.end_datetime < start_datetime:
                        continue
                    elif meet.start_datetime > end_datetime:
                        continue
                    else:
                        booking_reject = True
                        break
                if booking_reject:
                    continue
                else:
                    bookings.append(Doctors.objects.get(id=d))
                    break

            if not bookings:
                return Response(status=404)

            else:
                assigned_doctor = bookings[0]

            meet = Meet.objects.create(
                patient_id=patient, start_datetime=start_datetime, end_datetime=end_datetime,
                assigned_doctor=assigned_doctor, service=service)
            meet.save()

            return Response(status=201)

        else:
            return Response(status=400)


class GetByZipcode(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        zipcode = request.data.get('zipcode')
        doctors = Meet.objects.all().values_list('assigned_doctor', flat=True)
        doctors = list(set(doctors))
        doctors_list = Doctors.objects.filter(id__in=doctors, zipcode=zipcode).values_list('name')
        return Response(doctors_list)
