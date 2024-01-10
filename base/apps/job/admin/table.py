from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from ..models import Table


class CountListFilter(SimpleListFilter):
    title = 'Count'
    parameter_name = 'count'

    def lookups(self, request, model_admin):
        return (
            ('0', '0'),
            ('1', '1+'),
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(count=0)
        if self.value() == '1':
            return queryset.filter(count__gt=0)

class TableAdmin(admin.ModelAdmin):
    list_display = [
        "schemaname",
        "tablename",
        "count",
    ]
    list_filter = (CountListFilter,)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_edit_permission(self, request, obj=None):
        return False


admin.site.register(Table, TableAdmin)
