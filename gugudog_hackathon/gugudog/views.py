from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserForm
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

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            auth.login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
        else:
            form = UserForm()
            error = "아이디가 이미 존재합니다"
            return render(request, 'registration/signup.html', {'form': form, 'error': error})
    else:
        form = UserForm()
        return render(request, 'registration/signup.html', {'form': form})

# class ServiceAutocomplete(autocomplete.Select2QuerySetView):
#     def get_queryset(self):
#         if not self.request.user.is_authenticated():
#             return Service.objects.none()
        
#         qs = Service.objects.all()

#         if self.q:
#             qs = qs.filter(name__istartswith=self.q)

#         return qs

def add(request):
    
    form = AddForm()
    context = {
        'form' : form
    }
    return render(request, 'add.html', context)


def service_detail(request, service_slug):
    service = Service.objects.get(slug=service_slug)
    

