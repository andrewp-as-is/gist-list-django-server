from datetime import datetime

from django.contrib import admin
from django.template.defaultfilters import filesizeformat
from django.utils.timesince import timesince

from ..models import VacuumFullReport

class VacuumFullReportAdmin(admin.ModelAdmin):
    list_display = [
        'schemaname',
        'tablename',
        'size_before_pretty',
        'size_after_pretty',
        'time',
        'timesince'
    ]
    list_filter = [
        'schemaname',
    ]
    search_fields = [
        'schemaname',
        'tablename',
    ]

    def size_before_pretty(self,obj):
        return filesizeformat(obj.size_before_pretty)

    def size_after_pretty(self,obj):
        return filesizeformat(obj.size_after_pretty)

    def time(self,obj):
        return datetime.fromtimestamp(obj.timestamp)

    def timesince(self,obj):
        return timesince(datetime.fromtimestamp(self.timestamp))

admin.site.register(VacuumFullReport,VacuumFullReportAdmin)
