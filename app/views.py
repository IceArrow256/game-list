from django.shortcuts import render, redirect

import django.contrib.auth as DCA

import app.models as models
import app.forms as forms


def country(request):
    username = None
    games = models.Game.objects.all()
    if request.user.is_authenticated:
        username = request.user.username
    context = {'active': 'games', 'username': username, 'games': games}
    return render(request, 'app/games.html', context)

def games(request):
    username = None
    games = models.Game.objects.all()
    if request.user.is_authenticated:
        username = request.user.username
    context = {'active': 'games', 'username': username, 'games': games}
    return render(request, 'app/games.html', context)


def index(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    context = {'active': 'home', 'username': username}
    return render(request, 'app/index.html', context)


def add_country(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    if request.method == "POST":
        form = forms.CountryCreateForm(request.POST)
        if form.is_valid():
            country = form.save(commit=False)
            country.name = request.POST['name']
            country.save()
            return redirect('games')
    else:
        form = forms.CountryCreateForm(request.POST)
    return render(request, 'app/add.html', {'username': username, 'form': form, 'what': 'country'})

def add_platform(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    if request.method == "POST":
        form = forms.PlatformCreateForm(request.POST)
        if form.is_valid():
            platform = form.save(commit=False)
            platform.name = request.POST['name']
            platform.save()
            return redirect('games')
    else:
        form = forms.PlatformCreateForm(request.POST)
    return render(request, 'app/add.html', {'username': username, 'form': form, 'what': 'platform'})

def add_series(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    if request.method == "POST":
        form = forms.SeriesCreateForm(request.POST)
        if form.is_valid():
            series = form.save(commit=False)
            series.name = request.POST['name']
            series.save()
            return redirect('games')
    else:
        form = forms.SeriesCreateForm(request.POST)
    return render(request, 'app/add.html', {'username': username, 'form': form, 'what': 'series'})

def add_developer(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    if request.method == "POST":
        form = forms.DeveloperCreateForm(request.POST)
        if form.is_valid():
            developer = form.save(commit=False)
            developer.country = models.Country.objects.get(id=request.POST['country'])
            developer.name = request.POST['name']
            developer.save()
            return redirect('games')
    else:
        form = forms.DeveloperCreateForm(request.POST)
    return render(request, 'app/add.html', {'username': username, 'form': form, 'what': 'developer'})

def add_game(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    if request.method == "POST":
        form = forms.GameCreateForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.platform = models.Platform.objects.get(id=request.POST['platform'])
            game.series = models.Series.objects.get(id=request.POST['series'])
            game.developer = models.Developer.objects.get(id=request.POST['developer'])
            game.name = request.POST['name']
            game.release = request.POST['release']
            game.save()
           
            return redirect('games')
    else:
        form = forms.GameCreateForm(request.POST)
    return render(request, 'app/add.html', {'username': username, 'form': form.as_table, 'what': 'game'})


def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = DCA.authenticate(request, username=username, password=password)
        if user is not None:
            DCA.login(request, user)
            return redirect('/')
        else:
            form = DCA.forms.AuthenticationForm(request.POST)
            return render(request, 'app/login.html', {'active': 'login', 'form': form})
    else:
        form = DCA.forms.AuthenticationForm()
        return render(request, 'app/login.html', {'active': 'login', 'form': form})


def my_games(request):
    list_type = 'inbox'
    if request.method == 'GET':
        if 'list' in request.GET:
            list_type = request.GET['list']
    username = None
    game_type = models.GameType.objects.filter(
        name=list_type.capitalize()).first()
    games = models.GameList.objects.filter(
        user=request.user).filter(game_type=game_type)
    if request.user.is_authenticated:
        username = request.user.username
    context = {'active': 'my-games', 'username': username,
               'list': list_type.capitalize(), 'games': games}
    return render(request, 'app/my-games.html', context)


def profile(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    context = {'active': 'profile', 'username': username}
    return render(request, 'app/profile.html', context)


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = DCA.forms.UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = DCA.authenticate(username=username, password=password)
            DCA.login(request, user)
            return redirect('/')
        else:
            return render(request, 'app/sign-up.html', {'form': form})
    else:
        form = DCA.forms.UserCreationForm()
        return render(request, 'app/sign-up.html', {'active': 'sign-up', 'form': form})
