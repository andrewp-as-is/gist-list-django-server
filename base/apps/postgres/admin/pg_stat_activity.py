from django.contrib import admin

from ..models import PgStatActivity

class PgStatActivityAdmin(admin.ModelAdmin):
    list_display = [
        'pid',
        'application_name',
        'backend_start',
        'backend_type',
        'query_start',
        'state_change',
        'state',
        'query',
    ]
    list_filter = ['application_name','backend_type',]
    list_search = ['application_name','query',]


admin.site.register(PgStatActivity,PgStatActivityAdmin)


"""
    return self.model.objects.filter(
    backend_type='client backend'
    ).exclude(
    application_name__contains='pgAdmin'
    ).exclude(query__contains='pg_stat_activity').order_by('pid')
"""
