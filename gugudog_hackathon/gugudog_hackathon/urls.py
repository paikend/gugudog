"""gugudog_hackathon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from gugudog import views
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('service_all/', views.service_all, name="service_all"),
    path('accounts/logout/', views.logout, name="logout"),
    path('accounts/', include('allauth.urls')),
    path('signup/', views.signup, name="signup"),

    path('add/', views.add, name="add"),
    path('recommendation', views.recommendation, name="recommendation"),
    path('sevice_detail/<int:service_pk>/',
         views.service_detail, name='service_detail'),

    path('delete/<int:gudog_service_pk>/<int:model_service_pk>', views.delete_service, name="delete_service"),
    path('delete_zzim/<int:zzim_service_pk>/<int:model_service_pk>', views.delete_zzim, name="delete_zzim"),
    url(r'^zzim/$', views.zzim, name='zzim'), 

    path('mp/', views.mp, name="mp"),
]
