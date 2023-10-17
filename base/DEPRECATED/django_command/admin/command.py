from django.contrib import admin

from ..models import Command

class CommandAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'app',
    ]
    list_filter = [
        'app',
    ]
    search_fields = [
        'name',
        'app',
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Command,CommandAdmin)
