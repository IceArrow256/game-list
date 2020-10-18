import django.urls as DU
import django.contrib.auth.views as DCAV


import app.views as views

urlpatterns = [
    DU.path('', views.index, name='index'),
    DU.path("logout/", DCAV.LogoutView.as_view(), name="logout"),
]


