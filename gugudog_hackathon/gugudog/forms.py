from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'password')
        labels = {
            'email': (''),
            'username': (''),
            'password': (''),
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '이메일'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '아이디'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'비밀번호'})
        }