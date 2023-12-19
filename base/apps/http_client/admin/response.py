__all__ = ["ResponseAdmin"]

from datetime import datetime
import os

from django.contrib import admin
from django.utils.timesince import timesince

from ..models import Response


class ResponseAdmin(admin.ModelAdmin):
    list_display = [
        "host",
        "url",
        "status",
        "disk_path",
        "created_at",
        "time",
        "timesince",
    ]
    search_fields = [
        "url",
    ]

    def time(self, obj):
        return datetime.fromtimestamp(obj.created_at)

    def timesince(self, obj):
        return "%s ago" % timesince(datetime.fromtimestamp(obj.created_at))

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Response, ResponseAdmin)
