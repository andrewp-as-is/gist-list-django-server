from datetime import datetime

from django.contrib import admin

from ..models import SqlReport

class SqlReportAdmin(admin.ModelAdmin):
    list_display = [
        'sql',
        'duration',
        'time',
        'timestamp',
    ]
    search_fields = [
        'sql',
    ]

    def time(self,obj):
        return datetime.fromtimestamp(obj.timestamp)

    def timesince(self,obj):
        return '%s ago' % timesince(datetime.fromtimestamp(obj.timestamp))

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(SqlReport,SqlReportAdmin)
