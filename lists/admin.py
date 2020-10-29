from django.contrib import admin

import lists.models as LM

# Register your models here.

admin.site.register(LM.GameListType)
admin.site.register(LM.GameInList)