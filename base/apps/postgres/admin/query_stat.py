from django.contrib import admin

from ..models import QueryStat

class QueryStatAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'query',
        'count',
        'avg_duration',
        'min_duration',
        'max_duration',
    ]


admin.site.register(QueryStat,QueryStatAdmin)
