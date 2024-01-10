from datetime import datetime

from django.contrib import admin
from django.utils.timesince import timesince

from ..models import UserTableModification

class UserTableModificationAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "tablename",
        "modified_at",
    ]

    def time(self,obj):
        return datetime.fromtimestamp(obj.created_at)

    def timesince(self,obj):
        return '%s ago' % timesince(datetime.fromtimestamp(obj.created_at))

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_edit_permission(self, request, obj=None):
        return False


admin.site.register(UserTableModification, UserTableModificationAdmin)
