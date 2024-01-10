from datetime import datetime

from django.contrib import admin
from django.utils.timesince import timesince

from ..models import Token

class TokenAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "token",
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_edit_permission(self, request, obj=None):
        return False


admin.site.register(Token, TokenAdmin)
