import django.urls as DU
import lists.views as LV
import django.views.generic.base as DVGB

urlpatterns = [
    DU.path("lists", LV.lists, name="lists"),
    DU.path("lists/<str:category>", LV.lists, name="lists"),
    DU.path("create/GameInList/<int:id>", LV.create, name="create"),
    DU.path("update/GameInList/<str:category>/<int:id>", LV.update, name="update-game-in-list"),
]