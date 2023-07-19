from . import views
from django.urls import path

urlpatterns = [
    path('', views.doctorhome ,name="doctorhome"),
    path('prescription/', views.prescription ,name="prescription"),
    path('saveprescription/', views.saveprescription ,name="saveprescription"),
    path('allprescriptions/', views.allprescriptions ,name="allprescriptions"),
    path('seeprescription/', views.seeprescription ,name="seeprescription"),
    path('seepres/', views.seepres ,name="seepres"),
]