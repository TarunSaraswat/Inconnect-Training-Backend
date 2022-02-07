from unicodedata import name
from django.shortcuts import render
from rest_framework.decorators import api_view
from User import serializers
from User.models import Doctors, Patients
from .models import DoctorService, Meet
from django.http import HttpResponse
from .serializers import MeetSerializer
from rest_framework.response import Response
import datetime
import json
from django.core.serializers import serialize
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
# Create your views here.


class Create_Appointment(APIView):
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


class Update_Meet(APIView):
    authentication_classes=[BasicAuthentication]
    permission_classes=[IsAuthenticated]
    def put(self,request):
        patient_id = request.data.get('patient_id')
        service = request.data.get("service")
        assigned_doctor = request.data.get("assigned_doctor")
        try:
            user = Meet.objects.get(
                patient_id=patient_id, service=service, assigned_doctor=assigned_doctor)
        except Patients.DoesNotExist:
            return HttpResponse(status=404)

        user.booked = request.data.get("booked")
        user.save()
        return HttpResponse(status=200)

    def delete(self,request):
        patient_id = request.data.get('patient_id')
        service = request.data.get("service")
        assigned_doctor = request.data.get("assigned_doctor")
        booked = request.data.get("booked")
        try:
            user = Meet.objects.get(
                patient_id=patient_id, service=service, assigned_doctor=assigned_doctor, booked=booked)
        except Patients.DoesNotExist:
            return HttpResponse(status=404)

        user.delete()
        return HttpResponse(status=200)


@api_view(['PUT'])
def addRating(request):
    if request.method == "PUT":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        patient_id = body['patient_id']
        service = body["service"]
        assigned_doctor = body["assigned_doctor"]
        try:
            user = Meet.objects.get(
                patient_id=patient_id, service=service, assigned_doctor=assigned_doctor)
        except Patients.DoesNotExist:
            return HttpResponse(status=404)

        if user.done == True:
            user.rating = body["rating"]
            user.save()
            return Response(status=200)

        return Response(status=400)


class Get_By_Time(APIView):
    authentication_classes=[BasicAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        try:
            start_datetime = body["start_datetime"]
            end_datetime = body["end_datetime"]

        except:
            return HttpResponse(status=400)

        try:
            user = Meet.objects.filter(booked__range=[start_datetime, end_datetime]).values_list(
                'assigned_doctor', flat=True)
        except Meet.DoesNotExist:
            return HttpResponse(status=404)

        doctor_list = []
        user = list(set(user))
        for u in user:
            doctor_list.append(Doctors.objects.filter(
                id=u).values_list('name', flat=True))

        result = {str(user[i]): str(doctor_list[i][0]) for i in range(len(user))}
        return Response(result)



class Get_By_Service(APIView):
    authentication_classes=[BasicAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        try:
            service = body["service"]

        except:
            return HttpResponse(status=400)

        try:
            user = Meet.objects.filter(service=service).values_list(
                'assigned_doctor', flat=True)
        except Meet.DoesNotExist:
            return HttpResponse(status=404)

        doctor_list = []
        user = list(set(user))
        for u in user:
            doctor_list.append(Doctors.objects.filter(
                id=u).values_list('name', flat=True))

        result = {str(user[i]): str(doctor_list[i][0]) for i in range(len(user))}

        return Response(result)


class Get_By_Zipcode(APIView):
    authentication_classes=[BasicAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:
            doctors = Meet.objects.all().values_list('assigned_doctor', flat=True)
        except Meet.DoesNotExist:
            return HttpResponse(status=404)

        doctor_list = []
        zipcode=request.data.get('zipcode')
        print(zipcode)
        doctors=list(set(doctors))
        for u in doctors:
            doctor_list.append(Doctors.objects.filter(id=int(u),zipcode=int(zipcode)).values_list('name', flat=True))

        doctor_list = list(set(doctor_list))
        result = {i+1: str(doctor_list[i][0]) for i in range(len(doctor_list))}

        return Response(result)
