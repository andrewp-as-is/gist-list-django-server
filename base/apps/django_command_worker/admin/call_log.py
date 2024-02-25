from django.contrib import admin

from ..models import CallLog


class CallLogAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "created_at",
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_edit_permission(self, request, obj=None):
        return False


admin.site.register(CallLog, CallLogAdmin)
