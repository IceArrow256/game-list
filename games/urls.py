import django.urls as DU
import games.views as GV
import django.views.generic.base as DVGB

urlpatterns = [
    DU.path("games", GV.games, name="games")
]