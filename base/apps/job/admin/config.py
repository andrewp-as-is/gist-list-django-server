from django.contrib import admin

from ..models import Config

class ConfigAdmin(admin.ModelAdmin):
    pass

admin.site.register(Config, ConfigAdmin)
