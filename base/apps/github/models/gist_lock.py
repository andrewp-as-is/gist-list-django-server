__all__ = ['GistLock']

import time

from django.db import models


class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(ignore_conflicts=True)
        return super().bulk_create(objs,**kwargs)

class GistLock(models.Model):
    objects = Manager()

    gist = models.OneToOneField('github.Gist', related_name='+',on_delete=models.DO_NOTHING)
    created_at = models.IntegerField()

    class Meta:
        managed = False

    def get_seconds(self):
        return int(time.time())-self.timestamp
