from datetime import datetime

from django.contrib import admin
from django.template.defaultfilters import filesizeformat
from django.utils.timesince import timesince

from ..models import Size

class SizeAdmin(admin.ModelAdmin):
    list_display = [
        'regclass',
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
        'regclass',
    ]

    def size_before_pretty(self,obj):
        return filesizeformat(obj.size_before_pretty)
    size_before_pretty.short_description = "size_before_pretty"

    def size_after_pretty(self,obj):
        return filesizeformat(obj.size_after_pretty)
    size_after_pretty.short_description = "size_after_pretty"

    def time(self,obj):
        return datetime.fromtimestamp(obj.timestamp)
    time.short_description = "time"

    def timesince(self,obj):
        return timesince(datetime.fromtimestamp(self.timestamp))
    timesince.short_description = "timesince"

admin.site.register(Size,SizeAdmin)
