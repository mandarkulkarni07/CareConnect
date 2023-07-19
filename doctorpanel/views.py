from contextlib import nullcontext
from pydoc import doc
from django.utils import timezone
from unicodedata import name
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import auth, User
from django.contrib import messages
import accounts.views
from panel.models import Patient,History,Appointment
from .models import Doctor, Prescription

# Create your views here.
def doctorhome(request):
    if request.user.is_authenticated:
            if request.method == "POST":
                appos = Appointment.objects.get(Doctor = request.user.username,Patient = request.POST['patient'])
                appos.visited = True
                appos.save()
                messages.success(request,"Patient marked as Visited. ")
            appos = Appointment.objects.filter(Doctor=request.user.username, visited= False)
            patients = Patient.objects.all()
            allhistorys = History.objects.all()
            allpres = list()
            if Prescription.objects.filter(Doctor=request.user).exists():
                prep = Prescription.objects.filter(Doctor=request.user)
                for i in prep:
                    allpres.append(i.Patient)
            else:
                allpres = []
            print(allpres)
            params = {'appos':appos,'patients':patients,'allhistorys':allhistorys,'allpres':allpres}
            return render(request,'doctorhome.html',params)
        # else:
        #     messages.error(request,"Something went wrong")
        #     return redirect(accounts.views.logout)
    else:
        messages.error(request,"Please Login First")
        return redirect(accounts.views.login)

def prescription(request):
    if request.user.is_authenticated:
        # if request.user in Doctor.objects.all():
            if request.method == "POST":
                patient = request.POST['patient']
                if Prescription.objects.filter(Patient=patient,Doctor=request.user).exists():
                    request.session['patient'] = patient
                    return redirect(seeprescription)
                pat = Patient.objects.get(name=User.objects.get(username=patient))
                his = History.objects.get(patient=pat)
                params = {'patient':pat,'history':his}
                request.session['patient'] = patient
                print(request.session['patient'],request.session)
                return render(request,'prescription.html',params)
            else:
                messages.error(request,"Something went wrong")
                return redirect(doctorhome)
        # else:
        #     messages.error(request,"Something went wrong")
        #     return redirect(accounts.views.logout)
    else:
        messages.error(request,"Please Login First")
        return redirect(accounts.views.login)

def saveprescription(request):
    d = {}
    for i in request.POST:
        # print(i[:4],i[::-1][0])
        if i[0] != 'c':
            # print(i[::-1][0],d.keys())
            if i[::-1][0] in d.keys():
                if i[:4] == "Medi":
                    d[i[::-1][0]]['Medi'] = request.POST[i]
                elif i[:4] == "Dose":
                    d[i[::-1][0]]['Dose'] = request.POST[i]
                elif i[:4] == "Dura":
                    d[i[::-1][0]]['Dura'] = request.POST[i]
                else:
                    d[i[::-1][0]]['Quan'] = request.POST[i]
            else:
                d[i[::-1][0]] = {'Medi':request.POST[i]}
    pres = Prescription.objects.create(Patient=request.session['patient'],Doctor=request.user.username,Medicines=d,timestamp=timezone.now())
    pres.save()
    return redirect(seeprescription)

def seeprescription(request):
        patient = request.session['patient']
        doctor = request.user.username
        pres = Prescription.objects.get(Patient=patient,Doctor=doctor)
        patient = Patient.objects.get(name=User.objects.get(username=patient))
        params = {'pres':pres,'medicines':dict(pres.Medicines),'patient':patient}
        print(pres.Medicines,type(pres.Medicines))
        return render(request,'seeprescription.html',params)

def allprescriptions(request):
    if request.user.is_authenticated:
        # if request.user in Doctor.objects.all():
            appos = Appointment.objects.filter(Doctor=request.user.username)
            patients = Patient.objects.all()
            allhistorys = History.objects.all()
            allpres = list()
            if Prescription.objects.filter(Doctor=request.user).exists():
                prep = Prescription.objects.filter(Doctor=request.user)
                for i in prep:
                    allpres.append(i.Patient)
            else:
                allpres = []
            print(allpres)
            params = {'appos':appos,'patients':patients,'allhistorys':allhistorys,'allpres':allpres}
            return render(request,'allprescriptions.html',params)
        # else:
        #     messages.error(request,"Something went wrong")
        #     return redirect(accounts.views.logout)
    else:
        messages.error(request,"Please Login First")
        return redirect(accounts.views.login)

def seepres(request):
    patient = request.POST['patient']
    doctor = request.user.username
    pres = Prescription.objects.get(Patient=patient,Doctor=doctor)
    patient = Patient.objects.get(name=User.objects.get(username=patient))
    params = {'pres':pres,'medicines':dict(pres.Medicines),'patient':patient}
    print(params)
    return render(request,"seeprescription.html",params)