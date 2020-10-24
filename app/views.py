from django.shortcuts import render, get_object_or_404
 
import django.shortcuts as DS

import django.contrib.auth as DCA

import app.models as models
import app.forms as forms

def redirect(to, get=''):
    response = DS.redirect(to)
    response['Location'] += get
    return response


def country(request):
    username = None
    games = models.Game.objects.all()
    if request.user.is_authenticated:
        username = request.user.username
    context = {'active': 'games', 'username': username, 'games': games}
    return render(request, 'app/games.html', context)


def games(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    list_type = 'game'
    if request.method == 'GET':
        if 'list' in request.GET:
            list_type = request.GET['list']
    if list_type == "game":
        data = models.Game.objects.all()
    elif list_type == "platform":
        data = models.Platform.objects.all()
    elif list_type == "series":
        data = models.Series.objects.all()
    elif list_type == "developer":
        data = models.Developer.objects.all()
    elif list_type == "country":
        data = models.Country.objects.all()
    context = {'active': 'games', 'username': username,
               'list': list_type.capitalize(), 'data': data}
    return render(request, 'app/games.html', context)


def index(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    context = {'active': 'home', 'username': username}
    return render(request, 'app/index.html', context)


def add_country(request):
    if request.user.is_authenticated:
        username = request.user.username
    if request.method == "POST":
        form = forms.CountryCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('games', '?list=country')
    else:
        form = forms.CountryCreateForm(request.POST)
    return render(request, 'app/change.html', {'username': username, 'form': form, 'what': 'country', 'action': 'Add'})


def edit_country(request, country_id=None):
    if request.user.is_authenticated:
        username = request.user.username
    country = get_object_or_404(models.Country, pk=country_id)
    if request.method == "POST":
        form = forms.CountryCreateForm(request.POST, instance=country)
        if form.is_valid():
            form.save()
            return redirect('games', '?list=country')
    else:
        form = forms.CountryCreateForm(instance=country)
    return render(request, 'app/change.html', {'username': username, 'form': form, 'what': 'country', 'action': 'Edit'})


def page404(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    context = {'username': username}
    return render(request, 'app/404.html', context)


def add_platform(request):
    if request.user.is_authenticated:
        username = request.user.username
    if request.method == "POST":
        form = forms.PlatformCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('games', '?list=country')
    else:
        form = forms.PlatformCreateForm(request.POST)
    return render(request, 'app/change.html', {'username': username, 'form': form, 'what': 'platform', 'action': 'Add'})


def edit_platform(request, platform_id=None):
    if request.user.is_authenticated:
        username = request.user.username
    platform = get_object_or_404(models.Platform, pk=platform_id)
    if request.method == "POST":
        form = forms.PlatformCreateForm(request.POST, instance=platform)
        if form.is_valid():
            form.save()
            return redirect('games', '?list=platform')
    else:
        form = forms.PlatformCreateForm(instance=platform)
    return render(request, 'app/change.html', {'username': username, 'form': form, 'what': 'platform', 'action': 'Edit'})

def add_series(request):
    if request.user.is_authenticated:
        username = request.user.username
    if request.method == "POST":
        form = forms.SeriesCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('games', '?list=series')
    else:
        form = forms.SeriesCreateForm(request.POST)
    return render(request, 'app/change.html', {'username': username, 'form': form, 'what': 'series', 'action': 'Add'})


def edit_series(request, series_id=None):
    if request.user.is_authenticated:
        username = request.user.username
    series = get_object_or_404(models.Series, pk=series_id)
    if request.method == "POST":
        form = forms.SeriesCreateForm(request.POST, instance=series)
        if form.is_valid():
            form.save()
            return redirect('games', '?list=series')
    else:
        form = forms.SeriesCreateForm(instance=series)
    return render(request, 'app/change.html', {'username': username, 'form': form, 'what': 'series', 'action': 'Edit'})

def add_developer(request):
    if request.user.is_authenticated:
        username = request.user.username
    if request.method == "POST":
        form = forms.DeveloperCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('games', '?list=developer')
    else:
        form = forms.DeveloperCreateForm(request.POST)
    return render(request, 'app/change.html', {'username': username, 'form': form, 'what': 'developer', 'action': 'Add'})


def edit_developer(request, developer_id=None):
    if request.user.is_authenticated:
        username = request.user.username
    developer = get_object_or_404(models.Developer, pk=developer_id)
    if request.method == "POST":
        form = forms.DeveloperCreateForm(request.POST, instance=developer)
        if form.is_valid():
            form.save()
            return redirect('games', '?list=developer')
    else:
        form = forms.DeveloperCreateForm(instance=developer)
    return render(request, 'app/change.html', {'username': username, 'form': form, 'what': 'developer', 'action': 'Edit'})

def add_game(request):
    if request.user.is_authenticated:
        username = request.user.username
    if request.method == "POST":
        form = forms.GameCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('games', '?list=game')
    else:
        form = forms.GameCreateForm(request.POST)
    return render(request, 'app/change.html', {'username': username, 'form': form, 'what': 'game', 'action': 'Add'})


def edit_game(request, game_id=None):
    if request.user.is_authenticated:
        username = request.user.username
    game = get_object_or_404(models.Game, pk=game_id)
    if request.method == "POST":
        form = forms.GameCreateForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            return redirect('games', '?list=game')
    else:
        form = forms.GameCreateForm(instance=game)
    return render(request, 'app/change.html', {'username': username, 'form': form, 'what': 'game', 'action': 'Edit'})


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
