"""game_list URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
import django.urls as DU

urlpatterns = [
    DU.path('admin/', admin.site.urls),
    DU.path('', DU.include('games.urls')),
    DU.path('', DU.include('lists.urls')),
    DU.path('', DU.include('profile.urls')),
    DU.path('', DU.include('registration.urls')),
    DU.path('', DU.include('stats.urls')),
]