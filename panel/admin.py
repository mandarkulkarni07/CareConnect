from django.contrib import admin
from .models import Patient,Appointment,History
# Register your models here.

admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(History)