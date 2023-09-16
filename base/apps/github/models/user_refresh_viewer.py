__all__ = ['UserRefreshViewer']

import time

from django.db import models


class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(ignore_conflicts=True)
        return super().bulk_create(objs,**kwargs)

class UserRefreshViewer(models.Model):
    objects = Manager()

    user = models.OneToOneField('github.User', related_name='+',on_delete=models.CASCADE)
    viewer = models.OneToOneField('github.User', related_name='+',on_delete=models.CASCADE)
    timestamp = models.IntegerField()

    class Meta:
        managed = False
        unique_together = [('user', 'viewer',)]
