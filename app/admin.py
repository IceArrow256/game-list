from django.contrib import admin

import app.models as models

admin.site.register(models.Platform)
admin.site.register(models.Series)
admin.site.register(models.Country)
admin.site.register(models.Developer)
admin.site.register(models.Game)
admin.site.register(models.GameType)
admin.site.register(models.GameList)
