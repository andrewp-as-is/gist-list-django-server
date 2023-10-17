from django.contrib import admin

from ..models import DiscordWebhook

class DiscordWebhookAdmin(admin.ModelAdmin):
    list_display = [
        'url',
    ]
    search_fields = [
        'url',
    ]

admin.site.register(DiscordWebhook,DiscordWebhookAdmin)
