import django.urls as DU
import profile.views as PV
import django.views.generic.base as DVGB

urlpatterns = [
    DU.path("profile", PV.profile, name="profile")
]