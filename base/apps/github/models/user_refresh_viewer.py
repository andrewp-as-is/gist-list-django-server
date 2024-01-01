__all__ = ['UserRefreshViewer']

import time

from django.db import models



class UserRefreshViewer(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.OneToOneField('github.User', related_name='+',on_delete=models.DO_NOTHING)
    viewer = models.OneToOneField('github.User', related_name='+',on_delete=models.DO_NOTHING)
    created_at = models.IntegerField()

    class Meta:
        managed = False
        unique_together = [('user', 'viewer',)]
