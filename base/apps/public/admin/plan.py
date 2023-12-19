from django.contrib import admin

from ..models import Plan

class PlanAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'order',
    ]
    search_fields = [
        'name',
    ]

admin.site.register(Plan,PlanAdmin)
