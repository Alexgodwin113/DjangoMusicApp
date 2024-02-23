from django.urls import path
from . import views
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .forms import  UserCreationWithEmailForm
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.shortcuts import (get_object_or_404, render, redirect) 

# Create your views here.
def home(request):
    return HttpResponse(render(request, 'home.html'))

def contact(request):
    return HttpResponse(render(request, 'contact.html'))

def about(request):
    return HttpResponse(render(request, 'about.html'))

    
class RegisterUser(CreateView):
    model = User
    form_class = UserCreationWithEmailForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')