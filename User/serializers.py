from pyexpat import model
from attr import fields
from rest_framework import serializers
from .models import Doctors,Patients

# class PatientSerializer(serializers.Serializer):
#     # class Meta:
#     #     model=Patients
#     #     fields='__all__'
#     id = serializers.IntegerField()
#     email = serializers.EmailField(max_length=254)
#     name = serializers.CharField(max_length = 100)
#     city =  serializers.CharField(max_length = 100)
#     state = serializers.CharField(max_length = 100)
#     zipcode = serializers.IntegerField()
    
#     def create(self, validated_data):
#         return Patients.objects.create(validated_data)
    
#     def update(self, instance, validated_data):
#         instance.email=validated_data.get('email',instance.email)
#         instance.name=validated_data.get('name',instance.name)
#         instance.city=validated_data.get('city',instance.city)
#         instance.state=validated_data.get('state',instance.state)
#         instance.zipcode=validated_data.get('zipcode',instance.zipcode)
#         instance.save()
#         return instance
    
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Doctors
        fields=['email','name','city','state','zipcode']
        # exclude=['id']
        
        
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model=Patients
        fields=['email','name','city','state','zipcode']