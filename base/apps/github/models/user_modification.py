__all__ = ['UserModification']

import time

from django.db import models


class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(
                update_conflicts=True,
                unique_fields = ['user_id',],
                update_fields = ['timestamp']
            )
        return super().bulk_create(objs,**kwargs)

class UserModification(models.Model):
    objects = Manager()

    user = models.OneToOneField('github.User', related_name='+',on_delete=models.DO_NOTHING)
    timestamp = models.IntegerField()

    class Meta:
        managed = False

    def get_seconds(self):
        return int(time.time())-self.timestamp
