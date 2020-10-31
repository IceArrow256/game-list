from django.shortcuts import render, redirect, get_object_or_404

import datetime as DT

import django.http as DH
import django.db.models as DDM
import stats.utils as SU

import games.models as GM
import lists.models as LM
import lists.forms as LF


def get_games_in_list_dict(games_in_list):
    keys = ['Game', 'Platform', 'Series', 'Developer', 'Country',
            'Release', 'List', 'Finished', 'Score', 'Edit', 'Delete']
    data = []
    for game_in_list in games_in_list:
        if game_in_list.game.series:
            series = game_in_list.game.series
        else:
            series = ''
        if game_in_list.score:
            score = game_in_list.score
        else:
            score = ''
        if game_in_list.finished:
            finished = game_in_list.finished.isoformat()
        else:
            finished = ''
        data.append({'game': game_in_list.game.name,
                     'platform': game_in_list.game.platform.name,
                     'series': series,
                     'developer': game_in_list.game.developer.name,
                     'country': game_in_list.game.developer.country.name,
                     'release': game_in_list.game.release.isoformat(),
                     'game_list_type': game_in_list.game_list_type.name,
                     'finished': finished, 'score': score,
                     'id': game_in_list.id})
    return keys, data


def lists(request, category='All'):
    context = SU.get_context(request)
    keys = []
    data = []
    form = LF.FilterFormGamesInList(request.GET)
    games_in_list = LM.GameInList.objects.all().filter(user=request.user)
    game_list_type = LM.GameListType.objects.all()
    if category == 'All':
        game_list_type = None
    if category == 'Inbox':
        game_list_type = game_list_type.filter(name='Inbox').first()
    if category == 'Completed':
        game_list_type = game_list_type.filter(name='Completed').first()
    if category == 'Planning':
        game_list_type = game_list_type.filter(name='Planning').first()
    if category == 'Paused':
        game_list_type = game_list_type.filter(name='Paused').first()
    if category == 'Dropped':
        game_list_type = game_list_type.filter(name='Dropped').first()
    if game_list_type:
        games_in_list = games_in_list.filter(game_list_type=game_list_type)
    if form.is_valid():
        sort = form.cleaned_data.get('sort')
        platform = form.cleaned_data.get('platform')
        series = form.cleaned_data.get('series')
        developer = form.cleaned_data.get('developer')
        country = form.cleaned_data.get('country')
        game_list_type = form.cleaned_data.get('game_list_type')
        release = form.cleaned_data.get('release')
        finished = form.cleaned_data.get('finished')
        
    else:
        sort = form['sort'].initial
        platform = form['platform'].initial
        series = form['series'].initial
        developer = form['developer'].initial
        country = form['country'].initial
        game_list_type = form['game_list_type'].initial
        
        release = form['release'].initial
        finished = form['finished'].initial
    games_in_list = games_in_list.order_by(f'{sort}')
    if platform:
        games_in_list = games_in_list.filter(game__platform=platform)
    if series:
        games_in_list = games_in_list.filter(game__series=series)
    if developer:
        games_in_list = games_in_list.filter(game__developer=developer)
    if country:
        games_in_list = games_in_list.filter(game__developer__country=country)
    if game_list_type:
        games_in_list = games_in_list.filter(game_list_type=game_list_type)
    if release:
        release = int(release)
        games_in_list = games_in_list.filter(game__release__gte=DT.date(
            release, 1, 1), game__release__lt=DT.date(release+1, 1, 1))
    if finished:
        finished = int(finished)
        games_in_list = games_in_list.filter(finished__gte=DT.date(
            finished, 1, 1), finished__lt=DT.date(finished+1, 1, 1))

    keys, data = get_games_in_list_dict(games_in_list)
    context['keys'] = keys
    context['data'] = data
    context['form'] = form
    context['category'] = category
    return render(request, 'lists/lists.html', context)


def create(request, id):
    game = get_object_or_404(GM.Game, pk=id)
    game_list_type = LM.GameListType.objects.filter(name='Inbox').first()
    game_in_list = LM.GameInList.objects.filter(
        user=request.user, game=game).first()
    if game_in_list == None:
        game_in_list = LM.GameInList(
            user=request.user, game=game, game_list_type=game_list_type, score=0)
        game_in_list.save()
    return redirect('games')


def get_score(count, avg):
    n = 2
    print(count, n, avg)
    if count >= n:
        return round(count/(count+n)*avg+(n)/(count+n)*7.2453, 2)
    else:
        return None


def update(request, id, category = 'All'):
    context = SU.get_context(request)
    game_in_list = get_object_or_404(LM.GameInList, pk=id)
    if request.method == 'POST':
        form = LF.GameInListCreateForm(request.POST, instance=game_in_list)
        if form.is_valid():
            form.save()
            game = GM.Game.objects.get(pk=game_in_list.game.id)
            n = LM.GameInList.objects.all().filter(game=game).exclude(score=0).count()
            avg = LM.GameInList.objects.all().filter(game=game).exclude(score=0).aggregate(DDM.Avg('score'))
            game.score = get_score(n, avg['score__avg'])
            game.save()
            return redirect('lists', category)
    else:
        form = LF.GameInListCreateForm(instance=game_in_list)
    context['form'] = form
    context['action'] = 'Update'
    context['category'] = f'{game_in_list.game.name} in List'
    if request.user.is_authenticated:
        return render(request, 'games/change.html', context)
    else:
        return redirect('login')


def delete(request, id=None):
    game_in_list = get_object_or_404(LM.GameInList, pk=id)
    game = GM.Game.objects.get(pk=game_in_list.game.id)
    n = LM.GameInList.objects.all().filter(game=game).exclude(score=0).count()
    avg = LM.GameInList.objects.all().filter(game=game).exclude(score=0).aggregate(DDM.Avg('score'))
    game.score = get_score(n, avg['score__avg'])
    game.save()
    game_in_list.delete()
    return redirect('games')
