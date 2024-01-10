from datetime import datetime

from django.contrib import admin
from django.utils.timesince import timesince

from ..models import Query

class QueryAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'query',
        'duration',
        'created_at',
        'timesince'
    ]

    def time(self,obj):
        return datetime.fromtimestamp(obj.created_at)

    def timesince(self,obj):
        return '%s ago' % timesince(datetime.fromtimestamp(obj.created_at))


admin.site.register(Query,QueryAdmin)
