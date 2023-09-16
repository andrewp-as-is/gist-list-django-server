from django.contrib import admin

from ..models import SqlStat

class SqlStatAdmin(admin.ModelAdmin):
    list_display = [
        'sql',
        'avg_duration',
        'min_duration',
        'max_duration',
    ]
    search_fields = [
        'sql',
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(SqlStat,SqlStatAdmin)
