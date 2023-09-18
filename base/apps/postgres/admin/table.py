from django.contrib import admin

from ..models import Table

class TableAdmin(admin.ModelAdmin):
    list_display = [
        'schemaname',
        'tablename',
    ]
    list_filter = [
        'schemaname',
    ]
    search_fields = [
        'schemaname',
        'tablename',
    ]

admin.site.register(Table,TableAdmin)
