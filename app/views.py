from django.shortcuts import render

# Create your views here.


def games(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    context = {'active': 'games', 'username': username}
    return render(request, 'app/games.html', context)


def index(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    context = {'active': 'home', 'username': username}
    return render(request, 'app/index.html', context)

def login(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    context = {'active': 'login', 'username': username}
    return render(request, 'app/login.html', context)


def my_games(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    context = {'active': 'my-games', 'username': username}
    return render(request, 'app/my-games.html', context)

def profile(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    context = {'active': 'profile', 'username': username}
    return render(request, 'app/profile.html', context)


def sign_up(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    context = {'active': 'sign-up', 'username': username}
    return render(request, 'app/sign-up.html', context)

