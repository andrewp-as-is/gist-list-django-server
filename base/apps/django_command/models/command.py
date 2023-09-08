__all__ = ['Command',]

from django.db import models


class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(
                update_conflicts=True,
                unique_fields = ['name',],
                update_fields = ['duration','timestamp']
            )
        return super().bulk_create(objs,**kwargs)

class Command(models.Model):
    objects = Manager()

    name = models.TextField(unique=True)
    duration = models.FloatField()
    timestamp = models.IntegerField()

    class Meta:
        managed = False
        ordering = ('name', )
