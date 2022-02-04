from django.shortcuts import render
from itsdangerous import Serializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from tensorboard import errors
from .models import Doctors,Patients
from .serializers import PatientSerializer,DoctorSerializer
from django.http import HttpResponse

# Create your views here.

@api_view(['GET','PUT'])
def getUpdateUser(request,user_id):
    if request.method == "GET":
        try:
            user=Patients.objects.get(id=user_id)
        except Patients.DoesNotExist:
            return HttpResponse(status=404)
            # return Response({'status':404,'message':'User does not exist'})
        
        result=Patients.objects.get(id=user_id)
        serializer=PatientSerializer(result)
        return Response(serializer.data)

    elif request.method == "PUT":
        try:
            user=Patients.objects.get(id=user_id)
        except Patients.DoesNotExist:
            return HttpResponse(status=404)
            # return Response({'status':404,'message':'User does not exist'})
            
        serializer=PatientSerializer(user,data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["success"]="updated successfully"
            
            return HttpResponse(status=200)
            # return Response({'status':200,'message':'Created Successfully'})
        
        return HttpResponse(status=400)
        # return Response({'status':400,'message':'Given data is wrong'})

@api_view(['POST'])
def addUserPatient(request):
    serializer=PatientSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return HttpResponse(status=400)
        # return Response({'status':400,'errors':serializer.errors,'message':'Given data is wrong'})
        
    return HttpResponse(status=201)
    # return Response({'status':201,'message':'Created Successfully'})

# @api_view(['POST'])
# def addUpdateDoctor(request):
#     serializer=DoctorSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     else:
#         return Response({'status':400,'errors':serializer.errors,'message':'given data is wrong'})
        
#     return Response(serializer.data)

@api_view(['POST'])
def addUserDoctor(request):
    serializer=DoctorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return HttpResponse(status=400)
        # return Response({'status':400,'errors':serializer.errors,'message':'Given data is wrong'})
        
    return HttpResponse(status=201)