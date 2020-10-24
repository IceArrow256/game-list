from django.shortcuts import render
import django.http as DH

def home(request):
    return render(request, 'stats/home.html')