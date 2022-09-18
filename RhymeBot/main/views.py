from django.shortcuts import render
from django.forms import ModelForm
from django.urls import reverse
from django.http import HttpResponseRedirect
# Create your views here.
def index(request): 
    return render(request, "main/index.html")