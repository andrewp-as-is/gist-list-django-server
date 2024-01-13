__all__ = ['UserRefresh',]

from django.db import models

class UserRefresh(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField('github.User', related_name='+',on_delete=models.DO_NOTHING)
    refreshed_at = models.IntegerField()
    secret_refreshed_at = models.IntegerField()

    class Meta:
        managed = False
