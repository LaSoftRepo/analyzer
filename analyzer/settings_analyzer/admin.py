from django.contrib import admin
from .models import StatusSiteParse, Settings, StopWordList


admin.site.register(StopWordList)
admin.site.register(Settings)
admin.site.register(StatusSiteParse)