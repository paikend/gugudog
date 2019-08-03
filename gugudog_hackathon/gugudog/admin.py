from django.contrib import admin
from .models import Service, GuDogService, GuDog

# Register your models here.
admin.site.register(Service)
admin.site.register(GuDogService)
admin.site.register(GuDog)