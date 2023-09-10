from django.contrib import admin
from django.utils.timesince import timesince

from ..models import RepeatConfig

class RepeatConfigAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'seconds',
    ]
    search_fields = [
        'name',
    ]

admin.site.register(RepeatConfig,RepeatConfigAdmin)
