from datetime import datetime

from django.contrib import admin
from django.utils.timesince import timesince

from ..models import Status


class StatusAdmin(admin.ModelAdmin):
    list_display = [
        "postgres_vacuum_full",
        "refreshed_at",
        "time",
        "timesince",
    ]

    def time(self,obj):
        return datetime.fromtimestamp(obj.created_at)

    def timesince(self,obj):
        return '%s ago' % timesince(datetime.fromtimestamp(obj.created_at))

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_edit_permission(self, request, obj=None):
        return False


admin.site.register(Status, StatusAdmin)
