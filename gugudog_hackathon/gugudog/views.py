from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .forms import AddForm
from .models import Service, GuDogService, GuDog
from django.contrib.auth.decorators import login_required
from dal import autocomplete



# Create your views here.
@login_required(login_url='signup/')
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
        'error': '',
    }

    if request.method == "POST":   
        gudog_added, created = GuDogService.objects.get_or_create(
            user=request.user,
            service=Service.objects.get(pk=request.POST['service']),
            register_date=request.POST['register_date']
        )
        
        print(gudog_added)
        gudog_qs = GuDog.objects.filter(user=request.user)
        if gudog_qs.exists():
            gudog = gudog_qs[0]
            # 이미 해당 서비스를 구독했으면
            if gudog.services.filter(service__pk=gudog_added.service.pk).exists():
                context['error'] = '이미 추가된 서비스입니다'
                gudog_added.delete()
                return redirect('add')
            else:
                print(gudog_added)
                gudog.services.add(gudog_added)
                return redirect('home')
        else:
            gudog_added.save()
            gudog = GuDog.objects.create(user=request.user)
            gudog.services.add(gudog_added)
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
