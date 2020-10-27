from django.shortcuts import render

import datetime as DT

import django.http as DH
import django.contrib.auth.models as DCAM

import stats.utils as SU
import games.models as GM
    

def home(request):
    def get_key_fist(item):
        return item[0]
    def get_key_last(item):
        return item[-1]
    def get_years():
        years = []
        for year in GM.Game.objects.all().values('release'):
            if year not in years:
                years.append(int(year['release'].year))
        print(years)
        return years

    
    context = SU.get_context(request)
    # Global stats
    global_stats = []
    global_stats.append(('Countries', GM.Country.objects.all().count()))
    global_stats.append(('Developers', GM.Developer.objects.all().count()))
    global_stats.append(('Games', GM.Game.objects.all().count()))
    global_stats.append(('Platform', GM.Platform.objects.all().count()))
    global_stats.append(('Series', GM.Series.objects.all().count()))
    global_stats.append(('User', DCAM.User.objects.all().count()))
    global_stats = sorted(global_stats, key=get_key_last, reverse=True)
    context["global_stats"] = global_stats
    # Platform
    platforms = []
    for platform in GM.Platform.objects.all():
        platforms.append((platform, GM.Game.objects.all().filter(platform=platform).count()))
    platforms = sorted(platforms, key=get_key_last, reverse=True)[:10]
    context["platforms"] = platforms
    # Series
    series = []
    for _series in GM.Series.objects.all():
        series.append((_series, GM.Game.objects.all().filter(series=_series).count()))
    series = sorted(series, key=get_key_last, reverse=True)[:10]
    context["series"] = series
    # Developers
    developers = []
    for developer in GM.Developer.objects.all():
        developers.append((developer, GM.Game.objects.all().filter(developer=developer).count()))
    developers = sorted(developers, key=get_key_last, reverse=True)[:10]
    context["developers"] = developers
    # Years
    years = []
    for year in get_years():
        years.append((year, GM.Game.objects.all().filter(release__gte=DT.date(year, 1, 1), release__lt=DT.date(year+1, 1, 1)).count()))
    years = sorted(years, key=get_key_fist, reverse=True)[:10]
    context["years"] = years
    # Countries
    countries = []
    for country in GM.Country.objects.all():
        countries.append((country, GM.Game.objects.all().filter(developer__country=country).count()))
    countries = sorted(countries, key=get_key_last, reverse=True)[:10]
    context["countries"] = countries
    
    return render(request, 'stats/home.html', context)