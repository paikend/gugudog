from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def service_all(request):
    return render(request, 'service_all.html')