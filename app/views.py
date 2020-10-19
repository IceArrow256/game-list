from django.shortcuts import render, redirect

import django.contrib.auth as DCA

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
    context = {'active': 'login'}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = DCA.authenticate(request, username=username, password=password)
        if user is not None:
            DCA.login(request, user)
            return redirect("/")
        else:
            context['error'] = 'Login error'

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
    form = DCA.forms.UserCreationForm(request.POST)
    context = {'active': 'sign-up', 'form': form}
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            DCA.login(request, user)
            return redirect("/")

    return render(request, 'app/sign-up.html', context)
