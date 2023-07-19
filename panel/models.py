from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Patient(models.Model):
   name = models.OneToOneField(User,on_delete=models.CASCADE)
   gender = models.CharField(max_length=10)
   address = models.TextField(null=True,blank=True)
   date_of_Birth = models.DateField(null=True,blank=True)
   height = models.IntegerField(default=0)
   weight = models.IntegerField(default=0)
   phoneno = models.CharField(max_length=15) 
   martial = models.CharField(max_length=10)
   addedon = models.DateTimeField()

   def __str__(self):
    return self.name.username

class History(models.Model):
   patient = models.OneToOneField(Patient,on_delete=models.CASCADE)
   allergy = models.TextField(null=True,blank=True)
   dieases = models.TextField(null=True,blank=True)
   other = models.TextField(null=True,blank=True)
   operations = models.TextField(null=True,blank=True)
   currentmedications = models.TextField(null=True,blank=True)
   Exercise = models.CharField(null=True,blank=True,max_length=100)
   Eating = models.CharField(null=True,blank=True,max_length=100)
   Alcohol = models.CharField(null=True,blank=True,max_length=100)
   smoke = models.CharField(null=True,blank=True,max_length=100)
   Caffeine = models.CharField(null=True,blank=True,max_length=100)

   def __str__(self):
      return self.patient.name.username

class Appointment(models.Model):
   Patient = models.CharField(max_length=50)
   Doctor = models.CharField(max_length=50)
   Time = models.DateTimeField(null=True,blank=True)
   visited = models.BooleanField(default=False)
   
   def __str__(self):
      return self.Patient + " ( "+ self.Doctor + " ) "   