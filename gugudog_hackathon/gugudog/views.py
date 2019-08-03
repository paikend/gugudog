from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth


# Create your views here.
def home(request):
    return render(request, 'home.html')

def service_all(request):
    return render(request, 'service_all.html')

def signup(request):
    return render(request, 'registration/signup.html')

def logout(request):
    auth.logout(request)
    return redirect('signup')
