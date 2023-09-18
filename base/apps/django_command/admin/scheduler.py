from django.contrib import admin
from django.utils.timesince import timesince

from ..models import Scheduler

class SchedulerAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'seconds',
    ]
    search_fields = [
        'name',
    ]

admin.site.register(Scheduler,SchedulerAdmin)
