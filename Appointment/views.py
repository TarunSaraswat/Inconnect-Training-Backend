from unicodedata import name
from django.shortcuts import render
from rest_framework.decorators import api_view
from Appointment.filters import MeetFilter
from User import serializers
from User.models import Doctors, Patients
from .models import DoctorService, Meet
from django.http import HttpResponse
from .serializers import MeetSerializer
from rest_framework.response import Response
import datetime
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.mixins import   ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin
import json
from django.core.serializers import serialize
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets
from rest_framework import generics
from django.db.models import Q
# Create your views here.


class CreateAppointment(APIView):
    authentication_classes=[BasicAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self, request):
        patient_id = request.data.get('patient_id')
        service = request.data.get("service")
        start_datetime = request.data.get("start_datetime")
        start_datetime=datetime.datetime.strptime(start_datetime,"%Y-%m-%dt%H:%M:%S")
        end_datetime=start_datetime+datetime.timedelta(hours=1)
        patient = Patients.objects.get(id=patient_id)
        try:
            doctorAtZipcode = Doctors.objects.filter(zipcode=patient.zipcode)
        except:
            return HttpResponse(status=404)

        try:
            doctorService = DoctorService.objects.filter(service=service)
        except:
            return HttpResponse(status=404)

        doctor = []
        for doc in doctorAtZipcode:
            for docService in doctorService:
                if str(doc.id) == str(docService.doctor_id):
                    doctor.append(doc.id)

        if doctor == []:
            return HttpResponse(status=404)
        try:
            bookings=[]
            for d in doctor:

                flag=False
                doc_meet=Meet.objects.filter(assigned_doctor=d)
            
                for meet in doc_meet:
                    
                    if (meet.booked+datetime.timedelta(hours=1))<start_datetime:
                        continue
                    elif meet.booked>end_datetime:
                        continue
                    else:
                        flag=True
                        break
                if flag == True:
                    continue
                else:
                    bookings.append(Doctors.objects.get(id=d))
                    break
        except:
            return Response(status=404)

        print("bookings",bookings)
        if bookings == []:
            return Response(status=404)
            # alternative_time=[]
            # for d in doctor:
            #     #Time after start time
            #     temp_start_datetime=start_datetime+datetime.timedelta(hours=1)
            #     temp_end_datetime=end_datetime+datetime.timedelta(hours=1)
            #     print(d,"loop2")
            #     flag=False
            #     doc_meet=Meet.objects.filter(assigned_doctor=d).values_list('booked')
            #     time_diff=[]
            #     for meet in doc_meet:
            #         time_diff.append(temp_start_datetime-meet.booked)
            #     time_diff_min=min(time_diff)
            #         # bookings.append(Meet.objects.get(~Q(booked__range=[start_datetime, end_datetime]),Q(assigned_doctor=d)).values_list('assigned_doctor'))
            #     for meet in doc_meet:
                    
            #         if (meet.booked+datetime.timedelta(hours=1))<temp_start_datetime:
            #             continue
            #         elif meet.booked>temp_end_datetime:
            #             continue
            #         else:
            #             flag=True
            #             break
            #     if flag == True:
            #         pass
            #     else:
            #         alternative_time.append(temp_start_datetime)
            #         if len(alternative_time)==3:
            #             result={"time_one":alternative_time[0],"time_two":alternative_time[1],"time_three":alternative_time[2]}
            #             return Response(result)
            #      # Time before start time
            #     start_datetime=start_datetime-datetime.timedelta(hours=1)
            #     end_datetime=end_datetime-datetime.timedelta(hours=1)
            #     print(d,"loop2")
            #     flag=False
            #     doc_meet=Meet.objects.filter(assigned_doctor=d)
            #         # bookings.append(Meet.objects.get(~Q(booked__range=[start_datetime, end_datetime]),Q(assigned_doctor=d)).values_list('assigned_doctor'))
            #     for meet in doc_meet:
                    
            #         if (meet.booked+datetime.timedelta(hours=1))<start_datetime:
            #             continue
            #         elif meet.booked>end_datetime:
            #             continue
            #         else:
            #             flag=True
            #             break
            #     if flag == True:
            #         continue
            #     else:
            #         alternative_time.append(start_datetime)
            #         if len(alternative_time)==3:
            #             result={"time_one":alternative_time[0],"time_two":alternative_time[1],"time_three":alternative_time[2]}
            #             return Response(result)
        else:
            assigned_doctor=bookings[0]
        print(assigned_doctor,"doc")
        meet = Meet.objects.create(
            patient_id=patient, booked=start_datetime, assigned_doctor=assigned_doctor, service=service)
        meet.save()

        return HttpResponse(status=201)
    
    def get(self,request):
        patient_id = request.data.get("patient_id")
        service = request.data.get("service")
        print(patient_id, service)
        try:
            user = Meet.objects.filter(patient_id=patient_id, service=service)
        except Meet.DoesNotExist:
            return HttpResponse(status=404)

        serializer = MeetSerializer(user, many=True)
        return Response(serializer.data)


# class GetUpdateMeet(GenericAPIView,ListModelMixin,RetrieveModelMixin,UpdateModelMixin):
#     queryset = Meet.objects.all()
#     serializer_class = MeetSerializer
#     permission_classes = [IsAuthenticated]

#     def get(self, request,*args,**kwargs):
#         return self.retrieve(request,*args,**kwargs)
    
#     def put(self,request,*args,**kwargs):
#         return self.update(request,*args,**kwargs)



class AddRating(GenericAPIView,UpdateModelMixin):
    queryset=Meet.objects.all().filter(done=True)
    serializer_class = MeetSerializer
    permission_classes = [IsAuthenticated]
    
    def put(self,request,*args,**kwargs):
        return self.partial_update(request,*args,**kwargs)


class MeetViewSet(viewsets.ModelViewSet):
    serializer_class = MeetSerializer
    permission_classes = [IsAuthenticated]
    queryset=Meet.objects.all()
    filter_backends=[DjangoFilterBackend]
    filter_class=MeetFilter
    
    def list(self,request,*args,**kwargs):
        obj=self.filter_queryset(self.get_queryset()).values_list('assigned_doctor',flat=True)
        doc=Doctors.objects.filter(id__in=obj).values_list('name')
        return Response(doc)
    
    def create(self,request,*args,**kwargs):
        pass


class GetByZipcode(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        zipcode=request.data.get('zipcode')
        doctors = Meet.objects.all().values_list('assigned_doctor', flat=True)
        doctors=list(set(doctors))
        doctors_list=Doctors.objects.filter(id__in=doctors,zipcode=zipcode).values_list('name')
        return Response(doctors_list)
