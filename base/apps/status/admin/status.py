from django.contrib import admin

from ..models import Status

class StatusAdmin(admin.ModelAdmin):
    list_display = [
        'healthcheck_success',
        'incidents_count',
    ]

admin.site.register(Status,StatusAdmin)
