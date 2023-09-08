from datetime import datetime

from django.contrib import admin
from django.template.defaultfilters import filesizeformat
from django.utils.timesince import timesince

from ..models import RefreshInfo

class RefreshInfoAdmin(admin.ModelAdmin):
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
        return datetime.fromtimestamp(obj.called_at)
    time.short_description = "time"

    def timesince(self,obj):
        return '%s ago' % timesince(datetime.fromtimestamp(obj.called_at))
    timesince.short_description = "timesince"

admin.site.register(RefreshInfo,RefreshInfoAdmin)
