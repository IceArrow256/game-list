from django.shortcuts import render

import stats.utils as SU

def profile(request):
    context = SU.get_context(request)
    return render(request, 'profile/profile.html', context)