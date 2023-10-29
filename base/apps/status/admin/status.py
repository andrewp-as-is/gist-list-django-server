from django.contrib import admin

from ..models import Status


class StatusAdmin(admin.ModelAdmin):
    list_display = [
        "healthcheck_success",
        "incidents_count",
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_edit_permission(self, request, obj=None):
        return False


admin.site.register(Status, StatusAdmin)
