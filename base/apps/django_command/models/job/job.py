__all__ = ['Job']

from django.db import models

class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(
                update_conflicts=True,
                unique_fields = ['name',],
                update_fields = ['priority']
            )
        return super().bulk_create(objs,**kwargs)

class Job(models.Model):
    objects = Manager()

    name = models.TextField()
    priority = models.IntegerField(default=0)

    class Meta:
        managed = False

