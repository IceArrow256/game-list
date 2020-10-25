from django.shortcuts import render

import django.http as DH
import stats.utils as SU

def lists(request):
    context = SU.get_context(request)
    return render(request, 'lists/lists.html', context)