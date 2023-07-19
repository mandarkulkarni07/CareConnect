from unicodedata import name
from django.shortcuts import render,redirect
from django.contrib.auth.models import auth, User
from django.contrib import messages
from panel.views import home
from panel.models import Patient
from doctorpanel.models import Doctor
from django.utils import timezone
import doctorpanel.views
# Create your views here.
def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            user = auth.authenticate(username=user.username, password=password)
            if user is not None:
                auth.login(request, user)
                docs = Doctor.objects.all()
                for i in docs:
                    if i.name == user:
                        return redirect(doctorpanel.views.doctorhome)
                p = Patient.objects.get(name=user)
                if p.date_of_Birth == "" or p.height == 0 or p.weight == 0 or p.phoneno == "" or p.martial == "" :
                    return redirect(completeprofile)
                else:
                    return redirect(home)
            else:
                messages.error(request,"Invalid Credentials")
        else:
            messages.error(request,"User does not exist.")
    return render(request,'login.html')

def register(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        gender = request.POST['gender']
        address = request.POST['address']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password == cpassword:
            user = User.objects.create_user(username=fname+" "+lname, password=password, email=email, first_name=fname,last_name=lname)
            user.save()
            P = Patient.objects.create(name=user,gender=gender,address=address,addedon=timezone.now())
            P.save()
            messages.success(request, 'Sign-up successful. You can login now')
            return redirect(login)
        else:
            messages.error(request,"Password do not match.")
            params = {'fname':fname,'lname':lname,'email':email,'gender':gender,'address':address,'wp':True}
    else:
        params = dict()
    return render(request,"register.html",params)

def completeprofile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            phoneno = request.POST['phoneno']
            dob = request.POST['dob']
            height = request.POST['height']
            weight = request.POST['weight']
            martial = request.POST['martial']
            user = request.user
            p = Patient.objects.get(name=user)
            p.date_of_Birth = dob
            p.phoneno = phoneno
            p.height = height
            p.weight = weight
            p.martial = martial
            p.save()
            messages.success(request, 'Profile updated successfully')
            return redirect(home)
        else:
            fname = list((request.user.username.split(" ")))[0]
            lname = list((request.user.username.split(" ")))[1]
            params = {'fname':fname,'lname':lname}
            return render(request,'cprofile.html',params)
    else:
        messages.error(request,"Please Login First")
        return redirect(login)

def logout(request):
    auth.logout(request)
    messages.success(request,"Logged out successfully.")
    return redirect(login)