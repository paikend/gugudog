from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Service)
admin.site.register(GuDogService)
admin.site.register(GuDog)
admin.site.register(Zzim)
admin.site.register(ZzimService)

admin.site.register(Category)
admin.site.register(InterestService)
admin.site.register(Interest)
