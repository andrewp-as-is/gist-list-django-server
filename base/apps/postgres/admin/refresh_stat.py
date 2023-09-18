from datetime import datetime

from django.contrib import admin

from ..models import RefreshStat

class RefreshStatAdmin(admin.ModelAdmin):
    list_display = [
        'schemaname',
        'matviewname',
        'avg_duration',
        'min_duration',
        'max_duration',
    ]
    search_fields = [
        'schemaname',
        'matviewname',
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(RefreshStat,RefreshStatAdmin)
