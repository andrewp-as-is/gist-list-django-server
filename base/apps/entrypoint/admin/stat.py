from django.contrib import admin

from ..models import Stat


class StatAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "count",
        "avg_duration",
        "min_duration",
        "max_duration",
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_edit_permission(self, request, obj=None):
        return False


admin.site.register(Stat, StatAdmin)
