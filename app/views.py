from django.shortcuts import render

# Create your views here.

def index(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username

    context = {'active': 'home', 'username': username}
    return render(request, 'app/index.html', context)
