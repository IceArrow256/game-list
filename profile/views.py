from django.shortcuts import render

import datetime as DT

import stats.utils as SU

import games.models as GM
import lists.models as LM

def profile(request, category='All'):
    def get_key_fist(item):
        return item[0]

    def get_key_last(item):
        return item[-1]

    def get_years():
        years = []
        for year in GM.Game.objects.all().values('release'):
            if int(year['release'].year) not in years:
                years.append(int(year['release'].year))
        for year in LM.GameInList.objects.all().values('finished'):
            if year['finished'] and int(year['finished'].year) not in years: 
                years.append(int(year['finished'].year))
        return years
    context = SU.get_context(request)
    query = LM.GameInList.objects.all().filter(user=request.user)
    if category == 'All':
        pass
    else:
        query = query.filter(user=request.user, game_list_type=LM.GameListType.objects.filter(name=category).first())
    # Global stats
    global_stats = []
    global_stats.append(('Countries', query.values('game__developer__country__name').distinct().count()))
    global_stats.append(('Developers', query.values('game__developer__name').distinct().count()))
    global_stats.append(('Games', query.count()))
    global_stats.append(('Platform', query.values('game__platform__name').distinct().count()))
    global_stats.append(('Series', query.values('game__series__name').distinct().count()))
    global_stats = sorted(global_stats, key=get_key_last, reverse=True)
    context["global_stats"] = global_stats
    # Platform
    platforms = []
    for platform in GM.Platform.objects.all():
        result = query.filter(game__platform=platform).count()
        if result:
            platforms.append((platform, result))
    platforms = sorted(platforms, key=get_key_last, reverse=True)[:10]
    context["platforms"] = platforms
    # Series
    series = []
    for _series in GM.Series.objects.all():
        result = query.filter(game__series=_series).count()
        if result:
            series.append((_series, result))
    series = sorted(series, key=get_key_last, reverse=True)[:10]
    context["series"] = series
    # Developers
    developers = []
    for developer in GM.Developer.objects.all():
        result = query.filter(game__developer=developer).count()
        if result:
            developers.append((developer, result))
    developers = sorted(developers, key=get_key_last, reverse=True)[:10]
    context["developers"] = developers
    # Years
    years = []
    for year in get_years():
        result = query.filter(game__release__gte=DT.date(year, 1, 1), game__release__lt=DT.date(year+1, 1, 1)).count()
        if result:
            years.append((year, result))
    years = sorted(years, key=get_key_fist, reverse=True)[:10]
    context["years"] = years
    # Years finished
    years = []
    for year in get_years():
        result = query.filter(finished__gte=DT.date(year, 1, 1), finished__lt=DT.date(year+1, 1, 1)).count()
        if result:
            years.append((year, result))
    years = sorted(years, key=get_key_fist, reverse=True)
    context["years_finished"] = years
    # Countries
    countries = []
    for country in GM.Country.objects.all():
        result = query.filter(game__developer__country=country).count()
        if result:
            countries.append((country, result))
    context["countries"] = countries
    # Lists
    if category == 'All':
        lists = []
        for game_list_type in LM.GameListType.objects.all():
            result = query.filter(game_list_type=game_list_type).count()
            if result:
                lists.append((game_list_type, result))
        lists = sorted(lists, key=get_key_last, reverse=True)[:10]
        context["lists"] = lists
    context['category'] = category
    return render(request, 'profile/profile.html', context)
