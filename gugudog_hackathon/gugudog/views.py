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

    gudog = GuDogService.objects.filter(user=request.user)

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
    model = GuDogService.objects.all()
    form = AddForm()
    context = {
        'form' : form,
        'models': model,
    }

    if request.method == "POST":  
        gudog_added = GuDogService(user=request.user,
                                       service=Service.objects.get(pk=request.POST['service']),
                                       register_date=request.POST['register_date'])
        gudog_added.save()
        return redirect('home')
    else:
        return render(request, 'add.html', context)

def delete_service(request, gudog_service_pk):
    deletingService = GuDogService.objects.get(pk=gudog_service_pk)
    deletingService.delete()
    return redirect('home')
    # return render(request, 'add.html', context)


def service_detail(request, service_slug):
    service = Service.objects.get(slug=service_slug)
