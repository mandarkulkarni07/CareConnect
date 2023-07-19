from . import views
from django.urls import path

urlpatterns = [
    path('', views.home ,name="home"),
    path('history/', views.history ,name="history"),
    path('edithistory/', views.edithistory ,name="edithistory"),
    path('savehistory/', views.savehistory ,name="savehistory"),
    path('setdoctor/', views.setdoctor ,name="setdoctor"),
    path('setdr/', views.serdr ,name="setdr"),
    path('bookappointment/', views.bookappointment ,name="bookappointment"),
    path('alldoctors/', views.alldoctors ,name="alldoctors"),
]