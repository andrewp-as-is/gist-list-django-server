from django.contrib import admin

from ..models import PgFileSettings

class PgFileSettingsAdmin(admin.ModelAdmin):
    list_display = [
        'sourcefile',
        'sourceline',
        'seqno',
        'name',
        'setting',
        'applied',
        'error',
    ]
    list_filter = [
        'name',
    ]
    search_fields = [
        'name',
    ]

    def url(self,obj):
        url = "/frameworks/%s" % obj.slug
        return mark_safe('<a href="%s" target="_blank">%s</a>' % (url,url))
    url.short_description = "url"
    url.allow_tags = True


admin.site.register(PgFileSettings,PgFileSettingsAdmin)
