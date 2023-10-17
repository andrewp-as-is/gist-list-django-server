__all__ = ['UserFollowerOrderJob']

from django.db import models


class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(ignore_conflicts=True)
        result = super().bulk_create(objs,**kwargs)
        return result

class UserFollowerOrderJob(models.Model):
    objects = Manager()

    user_id = models.TextField(unique=True)

    class Meta:
        managed = False
