from datetime import datetime

from django.contrib import admin
from django.utils.timesince import timesince

from ..models import CallReport

class CallReportAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'duration',
        'time',
        'timesince',
    ]
    list_filter = [
        'name',
    ]
    search_fields = [
        'name',
    ]

    def time(self,obj):
        return datetime.fromtimestamp(obj.created_at)

    def timesince(self,obj):
        return '%s ago' % timesince(datetime.fromtimestamp(obj.created_at))

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(CallReport,CallReportAdmin)
