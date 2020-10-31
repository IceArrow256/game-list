import django.urls as DU
import games.views as GV
import django.views.generic.base as DVGB

urlpatterns = [
    DU.path("browse", GV.browse, name="browse"),
    DU.path("browse/<str:category>", GV.browse, name="browse"),
    DU.path("create/<str:category>", GV.create, name="create"),
    DU.path("update/<str:category>/<int:id>", GV.update, name="update"),
    DU.path("delete/<str:category>/<int:id>", GV.delete, name="delete")
]