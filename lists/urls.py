import django.urls as DU
import lists.views as LV
import django.views.generic.base as DVGB

urlpatterns = [
    DU.path("lists", LV.lists, name="lists")
]