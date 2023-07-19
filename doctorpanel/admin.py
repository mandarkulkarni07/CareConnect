from django.contrib import admin
from.models import Doctor,Doctorschedule,Prescription

# Register your models here.
admin.site.register(Doctor)
admin.site.register(Doctorschedule)
admin.site.register(Prescription)