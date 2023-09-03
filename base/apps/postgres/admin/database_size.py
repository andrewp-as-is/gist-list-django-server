from django.contrib import admin
from django.template.defaultfilters import filesizeformat

from ..models import DatabaseSize

class DatabaseSizeAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'size',
        'size_pretty',
    ]
    list_filter = [
        'name',
    ]
    search_fields = [
        'name',
    ]

    def size_pretty(self,obj):
        return filesizeformat(obj.size)
    size_pretty.short_description = "size_pretty"

admin.site.register(DatabaseSize,DatabaseSizeAdmin)
