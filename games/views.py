from django.shortcuts import render, redirect, get_object_or_404

import datetime as DT

import django.http as DH

import stats.utils as SU

import games.form as GF
import lists.views as LV
import games.models as GM
import lists.models as LM


def get_games_dict(games, user=None):
    keys = ['Name', 'Platform', 'Series', 'Developer',
            'Country', 'Release', 'Score', 'List', 'Edit', 'Delete']
    data = []
    for game in games:
        if game.series:
            series = game.series.name
        else:
            series = ''
        if game.score:
            score = game.score
        else:
            score = ''
        in_list = False
        in_list_id = None
        game_in_list = LM.GameInList.objects.all().filter(user=user, game=game).first()
        if user and game_in_list:
            in_list = True
            in_list_id = game_in_list.id
        data.append({'name': game.name, 'platform': game.platform.name,
                     'series': series, 'developer': game.developer.name,
                     'country': game.developer.country.name,
                     'release': game.release.isoformat(), 'score': score,
                     'id': (game.id, in_list, in_list_id)})
    return keys, data


def get_platforms_dict(platforms):
    keys = ['Name', 'Edit', 'Delete']
    data = []
    for platform in platforms:
        data.append({'name': platform.name, 'id': (platform.id,)})
    return keys, data


def get_series_dict(series):
    keys = ['Name', 'Edit', 'Delete']
    data = []
    for _series in series:
        data.append({'name': _series.name, 'id': (_series.id,)})
    return keys, data


def get_developers_dict(developers):
    keys = ['Name', 'Country', 'Edit', 'Delete']
    data = []
    for developer in developers:
        data.append({'name': developer.name, 'country': developer.country.name, 'id': (developer.id,)})
    return keys, data


def get_countries_dict(countries):
    keys = ['Name', 'Edit', 'Delete']
    data = []
    for country in countries:
        data.append({'name': country.name, 'id': (country.id,)})
    return keys, data


def create_form(request_type, category, instance=None):
    form = None
    if category == 'Game':
        form = GF.GameCreateForm(request_type, instance=instance)
    if category == 'Platform':
        form = GF.PlatformCreateForm(request_type, instance=instance)
    if category == 'Series':
        form = GF.SeriesCreateForm(request_type, instance=instance)
    if category == 'Developer':
        form = GF.DeveloperCreateForm(request_type, instance=instance)
    if category == 'Country':
        form = GF.CountryCreateForm(request_type, instance=instance)
    return form


def get_object(category, id):
    if category == 'Game':
        model = GM.Game
    if category == 'Platform':
        model = GM.Platform
    if category == 'Series':
        model = GM.Series
    if category == 'Developer':
        model = GM.Developer
    if category == 'Country':
        model = GM.Country
    return get_object_or_404(model, pk=id)


def games(request, category='Game'):
    context = SU.get_context(request)
    keys = []
    data = []
    form = None

    if category == 'Game':
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
        games = GM.Game.objects.all().order_by(f'{sort}')
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
            games = games.filter(release__gte=DT.date(
                release, 1, 1), release__lt=DT.date(release+1, 1, 1))
        if not request.user.is_authenticated:
            keys, data = get_games_dict(games)
        else:
            keys, data = get_games_dict(games, request.user)

    if category == 'Platform':
        form = GF.FilterFormName(request.GET)
        if form.is_valid():
            sort = form.cleaned_data.get('sort')
        else:
            sort = form['sort'].initial
        platforms = GM.Platform.objects.all().order_by(f'{sort}')
        keys, data = get_platforms_dict(platforms)

    if category == 'Series':
        form = GF.FilterFormName(request.GET)
        if form.is_valid():
            sort = form.cleaned_data.get('sort')
        else:
            sort = form['sort'].initial
        series = GM.Series.objects.all().order_by(f'{sort}')
        keys, data = get_series_dict(series)

    if category == 'Developer':
        form = GF.FilterFormContry(request.GET)
        if form.is_valid():
            sort = form.cleaned_data.get('sort')
            country = form.cleaned_data.get('country')
        else:
            sort = form['sort'].initial
            country = form['country'].initial
        developers = GM.Developer.objects.all().order_by(f'{sort}')
        if country:
            developers = developers.filter(country=country)
        keys, data = get_developers_dict(developers)

    if category == 'Country':
        form = GF.FilterFormName(request.GET)
        if form.is_valid():
            sort = form.cleaned_data.get('sort')
        else:
            sort = form['sort'].initial
        countries = GM.Country.objects.all().order_by(f'{sort}')
        keys, data = get_countries_dict(countries)
    if not request.user.is_authenticated and category != 'Game':
        keys = keys[:-2]
    elif not request.user.is_authenticated and category == 'Game':
        keys = keys[:-3]
    context['keys'] = keys
    context['data'] = data
    context['form'] = form
    context['category'] = category
    return render(request, 'games/games.html', context)


def create(request, category=None):
    context = SU.get_context(request)
    if request.method == 'POST':
        form = create_form(request.POST, category)
        if form.is_valid():
            form.save()
            return redirect('games', category)
    else:
        form = create_form(request.POST, category)
    context['form'] = form
    context['action'] = 'Create'
    context['category'] = category
    if request.user.is_authenticated:
        return render(request, 'games/change.html', context)
    else:
        return redirect('login')


def update(request, category='Game', id=None):
    if category == 'GameInList':
        return LV.update(request, id)
    context = SU.get_context(request)
    obj = get_object(category, id)
    if request.method == 'POST':
        form = create_form(request.POST, category, obj)
        if form.is_valid():
            form.save()
            return redirect('games', category)
    else:
        form = create_form(None, category, obj)
    context['form'] = form
    context['action'] = 'Update'
    context['category'] = category
    if request.user.is_authenticated:
        return render(request, 'games/change.html', context)
    else:
        return redirect('login')


def delete(request, category='Game', id=None):
    if category == 'GameInList':
        return LV.delete(request, id)
    get_object(category, id).delete()
    return redirect('games', category)
