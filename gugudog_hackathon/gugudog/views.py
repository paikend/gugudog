from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .forms import AddForm
from .models import Service, GuDogService, GuDog
from django.contrib.auth.decorators import login_required
from dal import autocomplete



# Create your views here.
# @login_required
def home(request):

    gudog = GuDog.objects.get_or_create(user=request.user)

    context = {
        'gudog' : gudog,
    }
    return render(request, 'home.html', context)

def service_all(request):
    services = Service.objects.all()

    context = {
        'services' : services,
    }
    return render(request, 'service_all.html', context)

def recommendation(request):
    return render(request, 'recommendation.html')

def signup(request):
    return render(request, 'registration/signup.html')

def logout(request):
    auth.logout(request)
    return redirect('signup')

def add(request):
    
    form = AddForm()
    context = {
        'form' : form
    }
    return render(request, 'add.html', context)


def service_detail(request, service_slug):
    service = Service.objects.get(slug=service_slug)
    
