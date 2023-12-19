__all__ = ['CallTime',]

from django.db import models


class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(
                update_conflicts=True,
                unique_fields = ['name',],
                update_fields = ['timestamp']
            )
        return super().bulk_create(objs,**kwargs)

class CallTime(models.Model):
    objects = Manager()

    name = models.CharField(unique=True,max_length=255)
    created_at = models.IntegerField()

    class Meta:
        managed = False
        ordering = ('name', )
