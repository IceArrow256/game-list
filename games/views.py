from django.shortcuts import render

import django.http as DH
import games.models as GM
import stats.utils as SU


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

def games(request, category="Games"):
    context = SU.get_context(request)
    keys = []
    data = []
    if category == "Games":
        games = GM.Game.objects.all().order_by("-release")
        keys, data = get_games_dict(games)
    if category == "Platforms":
        platforms = GM.Platform.objects.all().order_by("-name")
        keys, data = get_platforms_dict(platforms)
    if category == "Series":
        series = GM.Series.objects.all().order_by("-name")
        keys, data = get_series_dict(series)
    if category == "Developers":
        developers = GM.Developer.objects.all().order_by("-name")
        keys, data = get_developers_dict(developers)
    if category == "Countries":
        countries = GM.Country.objects.all().order_by("-name")
        keys, data = get_countries_dict(countries)
    context["keys"] = keys
    context["data"] = data
    return render(request, 'games/games.html', context)
