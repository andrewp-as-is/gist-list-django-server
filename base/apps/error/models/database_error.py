__all__ = ['DatabaseError',]

from django.db import models


class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(ignore_conflicts=True)
        return super().bulk_create(objs,**kwargs)

class DatabaseError(models.Model):
    objects = Manager()

    sql = models.TextField()
    message = models.TextField()
    timestamp = models.IntegerField()

    class Meta:
        managed = False
        ordering = ('-timestamp', )
