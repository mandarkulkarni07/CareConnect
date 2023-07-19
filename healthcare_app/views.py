from django.shortcuts import render,redirect
from django.contrib import messages

def aboutus(request):
    return render(request,"aboutus.html")

def contactus(request):
    if request.method == "POST":
        messages.success(request,"Your response submitted successfully. ")
    return render(request,'contactus.html')