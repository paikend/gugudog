# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from survey.forms import EmailForm
from survey.models import Email
from django.shortcuts import render, redirect


class ConfirmView(TemplateView):

    template_name = "survey/confirm.html"

    def get_context_data(self, **kwargs):
        context = super(ConfirmView, self).get_context_data(**kwargs)
        context["uuid"] = kwargs["uuid"]
        context["email"] = EmailForm()
        return context

    def post(self, request, *args, **kwargs):
        form = EmailForm(request.POST, user=request.user)
        length_of_email = len(request.POST['email'])

        if form.is_valid() and length_of_email > 0:
            print('valid')
            form.save()
            return redirect('http://www.gugudog.tk')
        
        else:
            print('not valid')
            return redirect('http://www.gugudog.tk')