from django.contrib import admin

from ..models import Run


class RunAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "created_at",
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_edit_permission(self, request, obj=None):
        return False


admin.site.register(Run, RunAdmin)
