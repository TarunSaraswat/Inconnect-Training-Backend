from django.shortcuts import render
from rest_framework.decorators import api_view
from sqlalchemy import null
from User import serializers
from User.models import Doctors,Patients
from .models import DoctorService, Meet
from django.http import HttpResponse
from .serializers import MeetSerializer
from rest_framework.response import Response
import datetime
import json
from django.core.serializers import serialize

# Create your views here.
@api_view(['GET'])
def getAppointmentPatient(request):
    if request.method == "GET":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        patient_id=body["patient_id"]
        service=body["service"]
        print(patient_id,service)   
        try:
            user=Meet.objects.filter(patient_id=patient_id,service=service)
        except Meet.DoesNotExist:
            return HttpResponse(status=404)
        
        # result=Meet.objects.filter(patient_id=patient_id,service=service)
        serializer=MeetSerializer(user,many=True)
        return Response(serializer.data)

@api_view(['POST'])
def createAppointment(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    patient_id = body['patient_id']
    service = body["service"]
    patient=Patients.objects.get(id=patient_id)
    try:
        doctorAtZipcode=Doctors.objects.filter(zipcode=patient.zipcode)
    except:
        return HttpResponse(status=404)
    
    try:
        doctorService=DoctorService.objects.filter(service=service)
    except:
        return HttpResponse(status=404)
    print(doctorAtZipcode)
    print(doctorService)
    doctor=null
    for doc in doctorAtZipcode:
        print(doc.id)
        for docService in doctorService:
            print(docService.doctor_id)
            if str(doc.id)==str(docService.doctor_id):
                doctor=doc
    print(doctor)
    if doctor is null:
        return HttpResponse(status=400)
    try:
        bookings=Meet.objects.get(assigned_doctor=doctor.id).order_by('booked')
    except:
        bookings=None
    if bookings is None:
        booked=datetime.datetime.now()
    else:
        booked=bookings[len(bookings)-1].booked
        hours_added = datetime.timedelta(hours = 1)
        booked=booked+hours_added
    
    print(doctor)
        
    meet=Meet.objects.create(patient_id=patient,booked=booked,assigned_doctor=doctor,service=service)
    meet.save()
    
    return HttpResponse(status=201)



@api_view(['PUT','DELETE'])
def updateMeet(request):
    if request.method == "PUT":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        patient_id = body['patient_id']
        service = body["service"]
        assigned_doctor=body["assigned_doctor"]
        try:
            user=Meet.objects.get(patient_id=patient_id,service=service,assigned_doctor=assigned_doctor)
        except Patients.DoesNotExist:
            return HttpResponse(status=404)
            
        
        # serializer=MeetSerializer(user,data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
            
        #     return HttpResponse(status=200)
        user.booked=body["booked"]
        user.save()
        return HttpResponse(status=200)
    
    if request.method == "DELETE":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        patient_id = body['patient_id']
        service = body["service"]
        assigned_doctor=body["assigned_doctor"]
        booked=body["booked"]
        try:
            user=Meet.objects.get(patient_id=patient_id,service=service,assigned_doctor=assigned_doctor,booked=booked)
        except Patients.DoesNotExist:
            return HttpResponse(status=404)
            
        
        # serializer=MeetSerializer(user,data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
            
        #     return HttpResponse(status=200)
        user.delete()
        return HttpResponse(status=200)
    
@api_view(['PUT'])
def addRating(request):
    if request.method == "PUT":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        patient_id = body['patient_id']
        service = body["service"]
        assigned_doctor=body["assigned_doctor"]
        try:
            user=Meet.objects.get(patient_id=patient_id,service=service,assigned_doctor=assigned_doctor)
        except Patients.DoesNotExist:
            return HttpResponse(status=404)
        
        if user.done==True:
            user.rating=body["rating"]
            user.save()
            return Response(status=200)
        
        return Response(status=400)
    
@api_view(['GET'])
def getAppointmentByTime(request):
    if request.method == "GET":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        booked=body["booked"]
 
        try:
            user=Meet.objects.filter(booked=booked)
        except Meet.DoesNotExist:
            return HttpResponse(status=404)
        
        # result=Meet.objects.filter(patient_id=patient_id,service=service)
        serializer=MeetSerializer(user,many=True)
        return Response(serializer.data)
    
