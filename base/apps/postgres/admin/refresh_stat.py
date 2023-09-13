from datetime import datetime

from django.contrib import admin
from django.template.defaultfilters import filesizeformat
from django.utils.timesince import timesince

from ..models import RefreshStat

class RefreshStatAdmin(admin.ModelAdmin):
    list_display = [
        'schemaname',
        'tablename',
        'avg_duration',
        'min_duration',
        'max_duration',
        'timestamp',
    ]
    list_filter = [
        'schemaname',
    ]
    search_fields = [
        'schemaname',
        'tablename',
    ]
    def time(self,obj):
        return datetime.fromtimestamp(obj.called_at)

    def timesince(self,obj):
        return '%s ago' % timesince(datetime.fromtimestamp(obj.called_at))

admin.site.register(RefreshStat,RefreshStatAdmin)
