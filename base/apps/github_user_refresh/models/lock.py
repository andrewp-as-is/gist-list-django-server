__all__ = ['Lock']

import time

from django.db import models


class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(
                update_conflicts=True,
                unique_fields = ['user_id',],
                update_fields = ['token_id','timestamp']
            )
        return super().bulk_create(objs,**kwargs)

class Lock(models.Model):
    objects = Manager()

    user = models.OneToOneField('github.User', related_name='+',on_delete=models.CASCADE)
    token_id = models.IntegerField()
    timestamp = models.IntegerField()

    class Meta:
        managed = False

    def get_seconds(self):
        return int(time.time())-self.timestamp
