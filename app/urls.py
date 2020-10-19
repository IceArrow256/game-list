import django.urls as DU
import django.contrib.auth.views as DCAV


import app.views as views

urlpatterns = [
    DU.path('games', views.games, name='games'),
    DU.path('', views.index, name='index'),
    DU.path('login', views.login, name='login'),
    DU.path('my-games', views.my_games, name='my-games'),
    DU.path('profile', views.profile, name='profile'),
    DU.path('sign-up', views.sign_up, name='sign-up'),
    DU.path("logout/", DCAV.LogoutView.as_view(), name="logout"),
]


