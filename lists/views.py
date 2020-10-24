from django.shortcuts import render

import django.http as DH

def list(request):
    return DH.HttpResponse("Hello, Django!")