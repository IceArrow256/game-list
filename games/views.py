from django.shortcuts import render

import django.http as DH
import stats.utils as SU

def games(request):
    context = SU.get_context(request)
    return render(request, 'games/games.html', context)