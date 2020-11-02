from django.shortcuts import render, redirect, get_object_or_404

import datetime as DT

import django.core.paginator as DCP
import django.http as DH

import games.form as GF
import games.models as GM
import lists.models as LM
import lists.views as LV


def get_games_dict(games, user=None):
    data = []
    for game in games:
        series = game.series
        score = game.score
        game_in_list_id = None
        game_in_list = LM.GameInList.objects.all().filter(user=user, game=game).first()
        if user and game_in_list:
            game_in_list_id = game_in_list.id
        data.append({'Name': game.name, 'data': {'Platform': game.platform.name,
                                                 'Series': series,
                                                 'Developer': game.developer.name,
                                                 'Country': game.developer.country.name,
                                                 'Release': game.release.isoformat()},
                     'Score': score,
                     'id': game.id,
                     'game_in_list_id': game_in_list_id})
    return data


def get_platforms_dict(platforms):
    data = []
    for platform in platforms:
        data.append({'Name': platform.name, 'id': platform.id})
    return data


def get_series_dict(series):
    data = []
    for _series in series:
        data.append({'Name': _series.name, 'id': _series.id})
    return data


def get_developers_dict(developers):
    data = []
    for developer in developers:
        data.append({'Name': developer.name, 'data': {
                     'Country': developer.country.name},
                     'id': developer.id})
    return data


def get_countries_dict(countries):
    data = []
    for country in countries:
        data.append({'Name': country.name, 'id': country.id, })
    return data


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


def browse(request, category='Game'):
    context = {}
    data = []
    form = None

    if category == 'Game':
        form = GF.FilterFormGames(request.GET)
        if form.is_valid():
            search = form.cleaned_data.get('search')
            sort = form.cleaned_data.get('sort')
            platform = form.cleaned_data.get('platform')
            series = form.cleaned_data.get('series')
            developer = form.cleaned_data.get('developer')
            country = form.cleaned_data.get('country')
            release = form.cleaned_data.get('release')
            not_in_my_list = form.cleaned_data.get('not_in_my_list')
        else:
            search = form['search'].initial
            sort = form['sort'].initial
            platform = form['platform'].initial
            series = form['series'].initial
            developer = form['developer'].initial
            country = form['country'].initial
            release = form['release'].initial
            not_in_my_list = form['not_in_my_list'].initial
        games = GM.Game.objects.all()
        if search:
            games = games.filter(name__contains=search)
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
        games = games.order_by(f'{sort}')
        if not request.user.is_authenticated:
            data = get_games_dict(games)
        else:
            if not_in_my_list:
                for game_in_list in LM.GameInList.objects.all().filter(user=request.user):
                    games = games.exclude(pk=game_in_list.game.pk)
            data = get_games_dict(games, request.user)
    if category == 'Platform':
        form = GF.FilterFormName(request.GET)
        if form.is_valid():
            search = form.cleaned_data.get('search')
            sort = form.cleaned_data.get('sort')
        else:
            search = form['search'].initial
            sort = form['sort'].initial
        platforms = GM.Platform.objects.all().order_by(f'{sort}')
        if search:
            platforms = platforms.filter(name__contains=search)
        data = get_platforms_dict(platforms)

    if category == 'Series':
        form = GF.FilterFormName(request.GET)
        if form.is_valid():
            search = form.cleaned_data.get('search')
            sort = form.cleaned_data.get('sort')
        else:
            search = form['search'].initial
            sort = form['sort'].initial
        series = GM.Series.objects.all().order_by(f'{sort}')
        if search:
            series = series.filter(name__contains=search)
        data = get_series_dict(series)

    if category == 'Developer':
        form = GF.FilterFormContry(request.GET)
        if form.is_valid():
            search = form.cleaned_data.get('search')
            sort = form.cleaned_data.get('sort')
            country = form.cleaned_data.get('country')
        else:
            search = form['search'].initial
            sort = form['sort'].initial
            country = form['country'].initial
        developers = GM.Developer.objects.all().order_by(f'{sort}')
        if search:
            developers = developers.filter(name__contains=search)
        if country:
            developers = developers.filter(country=country)
        data = get_developers_dict(developers)

    if category == 'Country':
        form = GF.FilterFormName(request.GET)
        if form.is_valid():
            search = form.cleaned_data.get('search')
            sort = form.cleaned_data.get('sort')
        else:
            search = form['search'].initial
            sort = form['sort'].initial
        countries = GM.Country.objects.all().order_by(f'{sort}')
        if search:
            countries = countries.filter(name__contains=search)
        data = get_countries_dict(countries)

    paginator = DCP.Paginator(data, 8)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context['data'] = page_obj
    context['form'] = form
    context['category'] = category
    return render(request, 'games/browse.html', context)


def create(request, category=None):
    context = {}
    if request.method == 'POST':
        form = create_form(request.POST, category)
        if form.is_valid():
            form.save()
            return render(request, 'close.html', context)
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
    context = {}
    obj = get_object(category, id)
    if request.method == 'POST':
        form = create_form(request.POST, category, obj)
        if form.is_valid():
            form.save()
            return render(request, 'close.html', context)
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
    response = {
    }
    return DH.JsonResponse(response)
