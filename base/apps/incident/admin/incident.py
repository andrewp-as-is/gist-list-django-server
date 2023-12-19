from datetime import datetime

from django.contrib import admin
from django.utils.timesince import timesince

from ..models import Incident

class IncidentAdmin(admin.ModelAdmin):
    list_display = [
        'message',
        'time',
        'timesince',
    ]

    def time(self,obj):
        return datetime.fromtimestamp(obj.created_at)

    def timesince(self,obj):
        return '%s ago' % timesince(datetime.fromtimestamp(obj.created_at))


admin.site.register(Incident,IncidentAdmin)
