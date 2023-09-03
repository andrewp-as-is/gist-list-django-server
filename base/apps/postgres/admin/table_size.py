from django.contrib import admin
from django.template.defaultfilters import filesizeformat

from ..models import TableSize

class TableSizeAdmin(admin.ModelAdmin):
    list_display = [
        'regclass',
        'schemaname',
        'tablename',
        'size',
        'size_pretty',
    ]
    list_filter = [
        'schemaname',
    ]
    search_fields = [
        'schemaname',
        'tablename',
    ]

    def size_pretty(self,obj):
        return filesizeformat(obj.size)
    size_pretty.short_description = "size_pretty"

admin.site.register(TableSize,TableSizeAdmin)
