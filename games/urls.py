import django.urls as DU
import games.views as GV
import django.views.generic.base as DVGB

urlpatterns = [
    DU.path("games", GV.games, name="games"),
    DU.path("games/<str:category>", GV.games, name="games"),
    DU.path("create/<str:category>", GV.create, name="create"),
    DU.path("update/<str:category>/<int:id>", GV.update, name="update"),
    DU.path("delete/<str:category>/<int:id>", GV.delete, name="delete")
]