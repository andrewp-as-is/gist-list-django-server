__all__ = ['ApiUserGistsPaginationJob']

from django.db import models


class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(ignore_conflicts=True)
        return super().bulk_create(objs,**kwargs)

class ApiUserGistsPaginationJob(models.Model):
    objects = Manager()

    user_id = models.IntegerField()

    class Meta:
        managed = False
