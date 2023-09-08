from datetime import datetime

from django.contrib import admin
from django.utils.timesince import timesince

from ..models import Matview

class MatviewAdmin(admin.ModelAdmin):
    list_display = [
        'regclass',
        'duration',
        'time',
        'timesince',
    ]
    list_filter = [
    ]
    search_fields = [
        'regclass',
    ]

    def time(self,obj):
        return datetime.fromtimestamp(obj.timestamp)
    time.short_description = "time"

    def timesince(self,obj):
        return '%s ago' % timesince(datetime.fromtimestamp(obj.timestamp))
    timesince.short_description = "timesince"

admin.site.register(Matview,MatviewAdmin)
