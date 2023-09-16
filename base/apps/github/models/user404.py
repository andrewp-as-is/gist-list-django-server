__all__ = ['User404']

from django.db import models


class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(
                update_conflicts=True,
                unique_fields = ['login',],
                update_fields = ['timestamp',]
            )
        return super().bulk_create(objs,**kwargs)

class User404(models.Model):
    objects = Manager()

    login = models.TextField(unique=True)
    timestamp = models.IntegerField()

    class Meta:
        managed = False
