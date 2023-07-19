from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Doctor(models.Model):
    name = models.OneToOneField(User,on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    address = models.TextField(null=True,blank=True)
    date_of_Birth = models.DateField(null=True,blank=True)
    phoneno = models.CharField(max_length=15) 
    degree = models.CharField(max_length=200)
    speciality = models.CharField(max_length=100)
    status = models.CharField(default="Active",max_length=10)
    addedon = models.DateTimeField()

    def __str__(self):
        return self.name.username

class Doctorschedule(models.Model):
    Doctor = models.OneToOneField(Doctor,on_delete=models.CASCADE)
    Daysavail = models.CharField(max_length=50)
    Startime = models.TimeField(null=True,blank=True)
    Endtime = models.TimeField(null=True,blank=True)
    averageconsultime = models.IntegerField(null=True,blank=True)
    lastime = models.TimeField(null=True,blank=True)

    def __str__(self):
        return self.Doctor.name.username

class Prescription(models.Model):
    Patient = models.CharField(max_length=50)
    Doctor = models.CharField(max_length=50)
    Medicines = models.JSONField()
    timestamp = models.DateTimeField(null=True,blank=True)

    def __str__(self):
      return self.Doctor + " ( "+ self.Patient + " ) "   