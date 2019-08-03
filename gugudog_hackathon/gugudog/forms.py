from django import forms
from django.contrib.auth.models import User
from .models import Service, GuDog, GuDogService
from dal import autocomplete

class AddForm(forms.ModelForm):
    class Meta:
        model = GuDogService
        fields = ('service', 'register_date')
        labels = {
            'service': ('서비스 이름'),
            'register_date': ('구독 시작일')
        }
        widgets = {
            'service' :autocomplete.ModelSelect2Multiple(
            )
        }
    # test = forms.ModelChoiceField(queryset = Service.objects.all())
