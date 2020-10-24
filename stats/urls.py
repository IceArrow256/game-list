import django.urls as DU
import stats.views as SV
import django.views.generic.base as DVGB

urlpatterns = [
    DU.path("", SV.home, name="home")
]