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
    DU.path('edit-country/<int:country_id>', views.edit_country, name='edit-country'),
    DU.path('add-platform', views.add_platform, name='add-platform'),
    DU.path('edit-platform/<int:platform_id>', views.edit_platform, name='edit-platform'),
    DU.path('add-game', views.add_game, name='add-game'),
    DU.path('edit-game/<int:game_id>', views.edit_game, name='edit-game'),
    DU.path('404', views.page404, name='404'),
    DU.path('add-developer', views.add_developer, name='add-developer'),
    DU.path('edit-developer/<int:developer_id>', views.edit_developer, name='edit-developer'),
    DU.path('add-series', views.add_series, name='add-series'),
    DU.path('edit-series/<int:series_id>', views.edit_series, name='edit-series'),
    DU.path('add-gamelist/<int:game_id>', views.add_gamelist, name='add-gamelist'),
    DU.path('edit-gamelist/<int:gamelist_id>', views.edit_gamelist, name='edit-gamelist'),
    DU.path("logout/", DCAV.LogoutView.as_view(), name="logout"),
]
# edit_gamelist
