from django.contrib import admin

from ..models import Config

class ConfigAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'output',
    ]
    search_fields = [
        'name',
    ]

admin.site.register(Config,ConfigAdmin)
