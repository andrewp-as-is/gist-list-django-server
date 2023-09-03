__all__ = ['VacuumFullJob']

from django.db import models

class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(ignore_conflicts=True)
        return super().bulk_create(objs,**kwargs)

class VacuumFullJob(models.Model):
    objects = Manager()

    regclass = models.TextField(unique=True)

    class Meta:
        managed = False

