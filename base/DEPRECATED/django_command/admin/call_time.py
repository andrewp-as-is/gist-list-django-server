from datetime import datetime

from django.contrib import admin
from django.utils.timesince import timesince

from ..models import CallTime

class CallTimeAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'time',
        'timesince',
    ]
    search_fields = [
        'name',
    ]

    def time(self,obj):
        return datetime.fromtimestamp(obj.created_at)

    def timesince(self,obj):
        return '%s ago' % timesince(datetime.fromtimestamp(obj.created_at))

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(CallTime,CallTimeAdmin)
