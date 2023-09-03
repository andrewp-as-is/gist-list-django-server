from datetime import datetime

from django.contrib import admin
from django.template.defaultfilters import filesizeformat
from django.utils.timesince import timesince

from ..models import PythonError

class PythonErrorAdmin(admin.ModelAdmin):
    list_display = [
        'filename',
        'lineno',
        'count',
        'exc_type',
        'exc_message',
        'exc_traceback',
        'time',
        'timesince'
    ]
    list_filter = [
        'exc_type',
        'filename',
    ]
    search_fields = [
        'regclass',
    ]

    def time(self,obj):
        return datetime.fromtimestamp(obj.timestamp)
    time.short_description = "time"

    def timesince(self,obj):
        return timesince(datetime.fromtimestamp(obj.timestamp))
    timesince.short_description = "timesince"

    def has_add_permission(self, request, obj=None):
        return False

    def has_edit_permission(self, request, obj=None):
        return False

admin.site.register(PythonError,PythonErrorAdmin)
