__all__ = ['UserRefreshLock']

from django.db import models

class UserRefreshLock(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', related_name='+',on_delete=models.DO_NOTHING)
    secret = models.BooleanField(null=True)

    class Meta:
        managed = False
        unique_together = ('user', 'secret',)
