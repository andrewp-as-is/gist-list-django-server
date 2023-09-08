from datetime import datetime

from django.contrib import admin
from django.utils.timesince import timesince

from ..models import CallStat

class CallStatAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'calls_count',
    ]
    search_fields = [
        'name',
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(CallStat,CallStatAdmin)
