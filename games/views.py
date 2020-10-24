from django.shortcuts import render

import django.http as DH

def games(request):
    return DH.HttpResponse("Hello, Django!")