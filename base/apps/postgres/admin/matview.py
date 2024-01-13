from datetime import datetime

from django.contrib import admin
from django.utils.timesince import timesince

from ..models import Matview

class MatviewAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'schemaname',
        'matviewname',
        'refreshed_at',
        'time',
        'timesince'
    ]
    list_filter = ['schemaname']

    def time(self,obj):
        return datetime.fromtimestamp(obj.refreshed_at)

    def timesince(self,obj):
        return '%s ago' % timesince(datetime.fromtimestamp(obj.refreshed_at))


admin.site.register(Matview,MatviewAdmin)
