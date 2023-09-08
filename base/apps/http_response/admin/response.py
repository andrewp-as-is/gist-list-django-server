from datetime import datetime

from django.contrib import admin
from django.utils.timesince import timesince

from ..models import Response

class ResponseAdmin(admin.ModelAdmin):
    list_display = [
        'domain',
        'url',
        'status',
        'relpath',
        'job_priority',
        'time',
        'timesince',
    ]
    search_fields = [
        'url',
    ]

    def time(self,obj):
        return datetime.fromtimestamp(obj.timestamp)
    time.short_description = "time"

    def timesince(self,obj):
        return '%s ago' % timesince(datetime.fromtimestamp(obj.timestamp))
    timesince.short_description = "timesince"

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Response,ResponseAdmin)
