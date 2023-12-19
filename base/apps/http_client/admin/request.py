__all__ = ["Request"]

from datetime import datetime
import os

from django.contrib import admin
from django.utils.timesince import timesince

from ..models import Request


class RequestAdmin(admin.ModelAdmin):
    list_display = [
        "host",
        "url",
        "method",
        "proxy",
        "allow_redirects",
        "max_redirects",
        "max_retries",
        "disk_path",
        "retries_count",
        "priority",
        "created_at",
        "created_at_time",
        "created_at_timesince",
    ]
    search_fields = [
        "host",
        "url",
        "method",
    ]

    def created_at_time(self, obj):
        if obj.created_at:
            return datetime.fromtimestamp(obj.created_at)

    def created_at_timesince(self, obj):
        if obj.created_at:
            return "%s ago" % timesince(datetime.fromtimestamp(obj.created_at))


admin.site.register(Request, RequestAdmin)
