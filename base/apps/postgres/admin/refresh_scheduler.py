from django.contrib import admin
from django.template.defaultfilters import filesizeformat

from ..models import RefreshScheduler

class RefreshSchedulerAdmin(admin.ModelAdmin):
    list_display = [
        'schemaname',
        'matviewname',
        'seconds',
    ]
    list_filter = [
        'schemaname',
    ]
    search_fields = [
        'schemaname',
        'matviewname'
    ]

admin.site.register(RefreshScheduler,RefreshSchedulerAdmin)
