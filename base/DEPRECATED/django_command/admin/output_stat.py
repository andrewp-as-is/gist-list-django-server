from django.contrib import admin

from ..models import OutputStat

class OutputStatAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'count',
        'total_size',
        'avg_size',
        'min_size',
        'max_size',
    ]
    search_fields = [
        'name',
    ]

admin.site.register(OutputStat,OutputStatAdmin)
