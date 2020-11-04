import datetime as DT

import django.core.paginator as DCP
import django.db.models as DDM
import django.http as DH
import django.shortcuts as DS

import games.models as GM
import lists.forms as LF
import lists.models as LM


def get_games_in_list_dict(games_in_list):
    data = []
    for game_in_list in games_in_list:
        data.append({'name': game_in_list.game.name,
                     'img': game_in_list.game.img,
                     'data': {
                         'Platform': game_in_list.game.platform.name,
                         'Series': game_in_list.game.series,
                         'Developer': game_in_list.game.developer.name,
                         'Country': game_in_list.game.developer.country.name,
                         'Release': game_in_list.game.release.isoformat(),
                         'Adding time': game_in_list.date.isoformat() if game_in_list.date else '',
                         'List type': game_in_list.game_list_type.name,
                         'Finished': game_in_list.finished.isoformat() if game_in_list.finished else ''},
                     'score': game_in_list.score,
                     'avg': game_in_list.game.score,
                     'id': game_in_list.id})
    return data


def lists(request, category='All'):
    context = {}
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
        search = form.cleaned_data.get('search')
        sort = form.cleaned_data.get('sort')
        platform = form.cleaned_data.get('platform')
        series = form.cleaned_data.get('series')
        developer = form.cleaned_data.get('developer')
        country = form.cleaned_data.get('country')
        game_list_type = form.cleaned_data.get('game_list_type')
        release = form.cleaned_data.get('release')
        finished = form.cleaned_data.get('finished')
    else:
        search = form['search'].initial
        sort = form['sort'].initial
        platform = form['platform'].initial
        series = form['series'].initial
        developer = form['developer'].initial
        country = form['country'].initial
        game_list_type = form['game_list_type'].initial
        release = form['release'].initial
        finished = form['finished'].initial
    if search:
        games_in_list = games_in_list.filter(game__name__contains=search)
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
    paginator = DCP.Paginator(get_games_in_list_dict(
        games_in_list.order_by(f'{sort}')), 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['data'] = page_obj
    context['form'] = form
    context['category'] = category
    return DS.render(request, 'lists/lists.html', context)


def create(request, id):
    game = DS.get_object_or_404(GM.Game, pk=id)
    game_list_type = LM.GameListType.objects.filter(name='Inbox').first()
    game_in_list = LM.GameInList.objects.filter(user=request.user,
                                                game=game).first()
    if not game_in_list:
        game_in_list = LM.GameInList(
            user=request.user, game=game, game_list_type=game_list_type, score=None)
        game_in_list.save()
    return DH.JsonResponse({"id": game_in_list.id})


def get_score(game):
    count = LM.GameInList.objects.all().filter(
        game=game).exclude(score=None).count()
    avg = LM.GameInList.objects.all().filter(game=game).exclude(
        score=None).aggregate(DDM.Avg('score'))['score__avg']
    n = 2
    if count >= n:
        game.score = round(count/(count+n)*avg+(n)/(count+n)*7.2453, 2)
    else:
        game.score = None
    game.save()


def update(request, id, category='All'):
    context = {}
    game_in_list = DS.get_object_or_404(LM.GameInList, pk=id)
    if request.method == 'POST':
        form = LF.GameInListCreateForm(request.POST, instance=game_in_list)
        if form.is_valid():
            form.save()
            get_score(game_in_list.game)
            return DS.render(request, 'close.html')
    else:
        form = LF.GameInListCreateForm(instance=game_in_list)
    context['form'] = form
    context['action'] = 'Update'
    context['category'] = f'{game_in_list.game.name} in List'
    if request.user.is_authenticated:
        return DS.render(request, 'games/change.html', context)
    else:
        return DS.redirect('login')


def delete(request, id=None):
    game_in_list = DS.get_object_or_404(LM.GameInList, pk=id)
    game = game_in_list.game
    game_in_list.delete()
    get_score(game)
    response = {
        "id": game_in_list.game.id
    }
    return DH.JsonResponse(response)
