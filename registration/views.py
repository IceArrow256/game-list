from django.shortcuts import render

import django.contrib.auth.forms as DCAF
import django.views as DV
import django.urls as DU


class UserChange(DV.generic.CreateView):
    form_class = DCAF.UserChangeForm
    success_url = DU.reverse_lazy('login')
    template_name = 'registration/login.html'


class SignUpView(DV.generic.CreateView):
    form_class = DCAF.UserCreationForm
    success_url = DU.reverse_lazy('login')
    template_name = 'registration/sign-up.html'
