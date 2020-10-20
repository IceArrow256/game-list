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
    DU.path('add-country', views.add_country, name='add-country'),
    DU.path('add-developer', views.add_developer, name='add-developer'),
    DU.path('add-platform', views.add_platform, name='add-platform'),
    DU.path('add-series', views.add_series, name='add-series'),
    DU.path('add-game', views.add_game, name='add-game'),
    DU.path("logout/", DCAV.LogoutView.as_view(), name="logout"),
]


