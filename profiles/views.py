from django.shortcuts import render

import django.http as DH

def profile(request):
    return DH.HttpResponse("Hello, Django!")