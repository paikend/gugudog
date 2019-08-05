from django.contrib import admin
from .models import Service, GuDogService, GuDog, Zzim, ZzimService


# Register your models here.
admin.site.register(Service)
admin.site.register(GuDogService)
admin.site.register(GuDog)
admin.site.register(Zzim)
admin.site.register(ZzimService)