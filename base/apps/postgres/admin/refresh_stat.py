from datetime import datetime

from django.contrib import admin
from django.template.defaultfilters import filesizeformat
from django.utils.timesince import timesince

from ..models import RefreshStat

class RefreshStatAdmin(admin.ModelAdmin):
    list_display = [
        'regclass',
        'avg_duration',
        'min_duration',
        'max_duration',
    ]
    list_filter = [
    ]
    search_fields = [
        'regclass',
    ]

admin.site.register(RefreshStat,RefreshStatAdmin)
