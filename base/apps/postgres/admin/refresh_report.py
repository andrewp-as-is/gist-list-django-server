from datetime import datetime

from django.contrib import admin
from django.template.defaultfilters import filesizeformat
from django.utils.timesince import timesince

from ..models import RefreshReport

class RefreshReportAdmin(admin.ModelAdmin):
    list_display = [
        'schemaname',
        'tablename',
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

    def timesince(self,obj):
        return '%s ago' % timesince(datetime.fromtimestamp(obj.called_at))

admin.site.register(RefreshReport,RefreshReportAdmin)
