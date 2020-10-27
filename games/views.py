from django.shortcuts import render, redirect

import datetime as DT

import django.http as DH

import stats.utils as SU

import games.form as GF
import games.models as GM


def get_games_dict(games):
    keys = ["Name", "Platform", "Series", "Developer",
            "Country", "Release", "Score"]
    data = []
    for game in games:
        if game.series:
            series = game.series.name
        else:
            series = ""
        if game.score:
            score = game.score
        else:
            score = ""
        data.append([game.name, game.platform.name, series,
                     game.developer.name, game.developer.country.name,
                     game.release.isoformat(), score])
    return keys, data


def get_platforms_dict(platforms):
    keys = ["Name"]
    data = []
    for platform in platforms:
        data.append([platform.name])
    return keys, data


def get_series_dict(series):
    keys = ["Name"]
    data = []
    for _series in series:
        data.append([_series.name])
    return keys, data


def get_developers_dict(developers):
    keys = ["Name", "Country"]
    data = []
    for developer in developers:
        data.append([developer.name, developer.country.name])
    return keys, data


def get_countries_dict(countries):
    keys = ["Name"]
    data = []
    for country in countries:
        data.append([country.name])
    return keys, data


def games(request, category="Game"):
    context = SU.get_context(request)
    keys = []
    data = []
    form = None

    if category == "Game":
        form = GF.FilterFormGames(request.GET)
        if form.is_valid():
            sort = form.cleaned_data.get('sort')
            platform = form.cleaned_data.get('platform')
            series = form.cleaned_data.get('series')
            developer = form.cleaned_data.get('developer')
            country = form.cleaned_data.get('country')
            release = form.cleaned_data.get('release')
        else:
            sort = form['sort'].initial
            platform = form['platform'].initial
            series = form['series'].initial
            developer = form['developer'].initial
            country = form['country'].initial
            release = form['release'].initial
        games = GM.Game.objects.all().order_by(f"{sort}")
        if platform:
            games = games.filter(platform=platform)
        if series:
            games = games.filter(series=series)
        if developer:
            games = games.filter(developer=developer)
        if country:
            games = games.filter(developer__country=country)
        if release:
            release = int(release)
            games = games.filter(release__gte=DT.date(release, 1, 1), release__lt=DT.date(release+1, 1, 1))
        keys, data = get_games_dict(games)

    if category == "Platform":
        form = GF.FilterFormName(request.GET)
        if form.is_valid():
            sort = form.cleaned_data.get('sort')
        else:
            sort = form['sort'].initial
        platforms = GM.Platform.objects.all().order_by(f"{sort}")
        keys, data = get_platforms_dict(platforms)
    
    if category == "Series":
        form = GF.FilterFormName(request.GET)
        if form.is_valid():
            sort = form.cleaned_data.get('sort')
        else:
            sort = form['sort'].initial
        series = GM.Series.objects.all().order_by(f"{sort}")
        keys, data = get_series_dict(series)

    if category == "Developer":
        form = GF.FilterFormContry(request.GET)
        if form.is_valid():
            sort = form.cleaned_data.get('sort')
            country = form.cleaned_data.get('country')
        else:
            sort = form['sort'].initial
            country = form['country'].initial
        developers = GM.Developer.objects.all().order_by(f"{sort}")
        if country:
            developers = developers.filter(country=country)
        keys, data = get_developers_dict(developers)

    if category == "Country":
        form = GF.FilterFormName(request.GET)
        if form.is_valid():
            sort = form.cleaned_data.get('sort')
        else:
            sort = form['sort'].initial
        countries = GM.Country.objects.all().order_by(f"{sort}")
        keys, data = get_countries_dict(countries)

    context["keys"] = keys
    context["data"] = data
    context["form"] = form
    context["category"] = category

    return render(request, 'games/games.html', context)

def create(request, category=None):
    context = SU.get_context(request)
    if category == "Game":
        form = GF.GameCreateForm()
    if category == "Platform":
        form = GF.PlatformCreateForm()
    if category == "Series":
        form = GF.SeriesCreateForm()
    if category == "Developer":
        form = GF.DeveloperCreateForm()
    if category == "Country":
        form = GF.CountryCreateForm()
    context["form"] = form
    context["action"] = "Create"
    context["category"] = category
    return render(request, 'games/change.html', context)

def update(request, category="Game", id=None):
    context = SU.get_context(request)
    return render(request, 'games/change.html', context)

def delete(request, category="Game", id=None):
    return redirect('games')

