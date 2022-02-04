from django.shortcuts import render
from django.views import View
from itsdangerous import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from tensorboard import errors
from .models import Doctors,Patients
from .serializers import PatientSerializer,DoctorSerializer
from django.http import HttpResponse

# Create your views here.

class Get_Update_Patient(APIView):
    def get(self,request,user_id):
        try:
            user=Patients.objects.get(id=user_id)
        except Patients.DoesNotExist:
            return HttpResponse(status=404)
        
        result=Patients.objects.get(id=user_id)
        serializer=PatientSerializer(result)
        return Response(serializer.data)

    def put(self,request,user_id):
        try:
            user=Patients.objects.get(id=user_id)
        except Patients.DoesNotExist:
            return HttpResponse(status=404)

        data={"email": request.data.get("email"),
	        "name": request.data.get("name"),
	        "city": request.data.get("city"),
	        "state": request.data.get("state"),
	        "zipcode": request.data.get("zipcode")}    
        serializer=PatientSerializer(user,data=data)
        
        if serializer.is_valid():
            serializer.save()
            data["success"]="updated successfully"
            
            return HttpResponse(status=200)     
        return HttpResponse(status=400)

class Register_Patient(APIView):
    def post(self,request,*args):
        data={	"email": request.data.get("email"),
	        "name": request.data.get("name"),
	        "city": request.data.get("city"),
	        "state": request.data.get("state"),
	        "zipcode": request.data.get("zipcode")}
        serializer=PatientSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            return HttpResponse(status=400)
       
        return HttpResponse(status=201)

class Register_Doctor(APIView):
    def post(self,request,*args):
        data={	"email": request.data.get("email"),
	        "name": request.data.get("name"),
	        "city": request.data.get("city"),
	        "state": request.data.get("state"),
	        "zipcode": request.data.get("zipcode")}
        serializer=DoctorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            return HttpResponse(status=400)
       
        return HttpResponse(status=201)