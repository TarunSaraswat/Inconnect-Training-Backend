from User.filter import DoctorFilter, PatientFilter
from .models import Doctors,Patients
from .serializers import PatientSerializer,DoctorSerializer
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import   ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin
    
class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patients.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filter_class = PatientFilter
    
    def put(self,request,*args,**kwargs):
        return self.partial_update(request,*args,**kwargs)    
    
class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctors.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filter_class = DoctorFilter
    
    def put(self,request,*args,**kwargs):
        return self.partial_update(request,*args,**kwargs)

# class GetUpdatePatient(GenericAPIView,RetrieveModelMixin,UpdateModelMixin):
#     queryset = Patients.objects.all()
#     serializer_class = PatientSerializer
#     permission_classes = [IsAdminUser]

#     def get(self, request,*args,**kwargs):
#         return self.retrieve(request,*args,**kwargs)
    
#     def put(self,request,*args,**kwargs):
#         return self.update(request,*args,**kwargs)

# class Register_Patient(GenericAPIView,CreateModelMixin):
#     queryset = Patients.objects.all()
#     serializer_class = PatientSerializer
#     permission_classes = [IsAdminUser]
    
#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)

# class Register_Doctor(GenericAPIView,ListModelMixin,CreateModelMixin):
#     queryset = Doctors.objects.all()
#     serializer_class = DoctorSerializer
#     permission_classes = [IsAdminUser]
    
#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)
    
#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)
    

    