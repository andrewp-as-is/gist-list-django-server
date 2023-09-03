__all__ = ['Healthcheck',]

from django.db import models


class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(
                update_conflicts=True,
                unique_fields = ['name'],
                update_fields = ['success','message','timestamp'],
            )
        return super().bulk_create(objs,**kwargs)

class Healthcheck(models.Model):
    objects = Manager()

    name = models.TextField(unique=True)
    success = models.BooleanField()
    message = models.TextField()
    timestamp = models.IntegerField()

    class Meta:
        managed = False
