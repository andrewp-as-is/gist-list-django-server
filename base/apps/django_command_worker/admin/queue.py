from django.contrib import admin

from ..models import Queue


class QueueAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "created_at",
    ]

admin.site.register(Queue, QueueAdmin)
