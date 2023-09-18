from django.contrib import admin

from ..models import Rule

class RuleAdmin(admin.ModelAdmin):
    list_display = [
        'schemaname',
        'tablename',
        'rulename',
        'event',
    ]
    list_filter = [
        'schemaname',
    ]
    search_fields = [
        'schemaname',
        'tablename',
        'rulename',
    ]

admin.site.register(Rule,RuleAdmin)
