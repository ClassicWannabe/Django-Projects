from django.shortcuts import render
from .forms import UserForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
# Create your views here.

class SignupView(CreateView):
    form_class = UserForm
    success_url = reverse_lazy('accounts:login_url')
    template_name = 'accounts/signup.html'
