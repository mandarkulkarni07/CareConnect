from contextlib import nullcontext
import re
from telnetlib import DO
from django.shortcuts import render,redirect
from django.contrib.auth.models import auth, User
from django.contrib import messages
import accounts.views
from datetime import datetime, timedelta, date
from django.utils import timezone
from doctorpanel.models import Doctor,Doctorschedule
from panel.models import Appointment, Patient,History

# Create your views here.
def texttolist(arr):
    if arr != None:
        l = arr.split(',')
        for j in l:
            if j == "":
                l.remove("")
        return l
    else:
        return list()


def listtotext(arr):
    l = ""
    for i in arr:
        l = l + str(i) + ","
    return l

def serdr(request):
    request.session['doctor'] = request.GET['dr']
    request.session['makeappointment'] = False
    return redirect(bookappointment)

def setdoctor(request):
    request.session['doctor'] = request.GET['dr']
    # check if history already taken or not
    if History.objects.filter(patient= Patient.objects.get(name=request.user)).exists():
        his = History.objects.get(patient= Patient.objects.get(name=request.user))
        request.session['makeappointment'] = True
        messages.success(request,"Patient history added automatically.")
        return redirect(bookappointment)
    else:
        return redirect(history)

def home(request):
    if request.user.is_authenticated:
        docs = Doctor.objects.all()
        docschedule = Doctorschedule.objects.all()
        if Appointment.objects.filter(Patient=request.user.username).exists():
            appos = Appointment.objects.filter(Patient=request.user.username)
            dctrs = list()
            for i in appos:
                dctrs.append(i.Doctor)
        else:
            dctrs = "null"
        params = {'docs':docs,'docschedule':docschedule,'appos':dctrs}
        return render(request,'home.html',params)
    else:
        messages.error(request,"Please Login First")
        return redirect(accounts.views.login)

def history(request):
    if request.user.is_authenticated:
        patient = Patient.objects.get(name=request.user)
        params = {'patient':patient}
        return render(request,'history.html',params)
    else:
        messages.error(request,"Please Login First")
        return redirect(accounts.views.login)

def bookappointment(request):
    patient = Patient.objects.get(name=request.user)
    doc = request.session['doctor']
    print(doc)
    doctor = Doctor.objects.get(name=User.objects.get(username=doc))
    appos = Appointment.objects.all()
    if  History.objects.filter(patient=patient).exists():
        j = History.objects.get(patient=patient)
    else:
        j = nullcontext
    if request.session['makeappointment'] == True :
        patient = Patient.objects.get(name=request.user)
        j = History.objects.get(patient=patient)
        dr = Doctor.objects.get(name = User.objects.get(username=request.session['doctor']))
        dctr = Doctorschedule.objects.get(Doctor=dr)
        today = date.today()
        d_start = datetime.combine(today, dctr.lastime)
        diff = timedelta(minutes=int(dctr.averageconsultime))
        d_end = diff + d_start
        request.session['makeappointment'] = False
        dctr.lastime = d_end.strftime('%H:%M:%S')
        dctr.save()
        obj = Appointment.objects.create(Patient=patient.name.username,Doctor= dr.name.username,Time=d_end)
        obj.save()
    return render(request,"booked.html",{'patient':patient,'j':j,'dr':doctor,'appos':appos})

def savehistory(request):
    if request.method == "POST":
        dieases = list()
        for i in request.POST:
            if request.POST[i] == str(1):
                dieases.append(i)
        n = User.objects.get(username=request.POST['patient'])
        patient = Patient.objects.get(name=n)
        allergy = request.POST['allergy']
        other = request.POST['other']
        operations = request.POST['operations']
        currentmedications = request.POST['currentmedications']
        Exercise = request.POST['Exercise']
        Eating = request.POST['Eating']
        Alcohol = request.POST['Alcohol']
        smoke = request.POST['smoke']
        Caffeine = request.POST['Caffeine']
        obj = History.objects.create(patient=patient,allergy=allergy,other=other,operations=operations,currentmedications=currentmedications,Exercise=Exercise,Eating=Eating,Alcohol=Alcohol,smoke=smoke,Caffeine=Caffeine,dieases=listtotext(dieases))
        obj.save()
        request.session['makeappointment'] = True
        messages.success(request,"Patient history added successfully")
        return redirect(bookappointment)
    else:
        messages.error(request,"Unknown error occured. ")
        return redirect(home)

def edithistory(request):
    if History.objects.filter(patient= Patient.objects.get(name=request.user)).exists():
        his = History.objects.get(patient= Patient.objects.get(name=request.user))
    else:
        messages.error(request,"Please make your 1st appointment ")
        return redirect(home)
    if request.method == "POST":
        dieases = list()
        for i in request.POST:
            if request.POST[i] == str(1):
                dieases.append(i)
        n = User.objects.get(username=request.POST['patient'])
        patient = Patient.objects.get(name=n)
        allergy = request.POST['allergy']
        other = request.POST['other']
        operations = request.POST['operations']
        currentmedications = request.POST['currentmedications']
        Exercise = request.POST['Exercise']
        Eating = request.POST['Eating']
        Alcohol = request.POST['Alcohol']
        smoke = request.POST['smoke']
        Caffeine = request.POST['Caffeine']
        his.allergy = allergy
        his.other = other
        his.operations = operations
        his.currentmedications = currentmedications
        his.Exercise = Exercise
        his.Eating = Eating
        his.Alcohol = Alcohol
        his.smoke = smoke
        his.Caffeine =Caffeine
        his.dieases=listtotext(dieases)
        his.save()
        messages.success(request,"History updated successfully")
        return redirect(home)
    return render(request,'edithistory.html',{'patient':Patient.objects.get(name=request.user),'his':his})

def alldoctors(request):
    drs = Doctor.objects.all()
    drschedule = Doctorschedule.objects.all()
    return render(request,'alldoctors.html',{'drs':drs,'drschedule':drschedule})