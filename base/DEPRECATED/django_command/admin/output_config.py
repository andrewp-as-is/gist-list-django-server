from django.contrib import admin

from ..models import OutputConfig

class OutputConfigAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'save',
    ]
    search_fields = [
        'name',
    ]

admin.site.register(OutputConfig,OutputConfigAdmin)
