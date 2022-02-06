from django.db import models


# Create your models here.

class Patients(models.Model):    
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=254)
    name = models.CharField(max_length = 100)
    city =  models.CharField(max_length = 100)
    state = models.CharField(max_length = 100)
    zipcode = models.IntegerField()
    
    def __str__(self) -> str:
        return str(self.id)
    
class Doctors(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=254)
    name = models.CharField(max_length = 100)
    city =  models.CharField(max_length = 100)
    state = models.CharField(max_length = 100)
    zipcode = models.IntegerField()

    def __str__(self) -> str:
        return str(self.id)