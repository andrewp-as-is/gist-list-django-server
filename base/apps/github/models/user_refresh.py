__all__ = ['UserRefresh']

from django.db import models

class UserRefresh(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.OneToOneField('github.User', related_name='+',on_delete=models.DO_NOTHING)
    secret = models.BooleanField()
    started_at = models.FloatField()
    finished_at = models.FloatField(null=True)

    class Meta:
        managed = False
        unique_together = [('user', 'secret',)]
