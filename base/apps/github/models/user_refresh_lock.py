__all__ = ['UserRefreshLock']

import time

from django.db import models


class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(ignore_conflicts=True)
        return super().bulk_create(objs,**kwargs)

class UserRefreshLock(models.Model):
    objects = Manager()

    user = models.OneToOneField('github.User', related_name='+',on_delete=models.DO_NOTHING)
    authenticated = models.BooleanField()
    timestamp = models.IntegerField()

    class Meta:
        managed = False
        unique_together = [('user', 'authenticated',)]

    def get_seconds(self):
        return int(time.time())-self.timestamp
