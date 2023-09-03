from django.contrib import admin
from django.utils.timesince import timesince

from ..models import Repeat

class RepeatAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'seconds',
    ]
    search_fields = [
        'name',
    ]

admin.site.register(Repeat,RepeatAdmin)
