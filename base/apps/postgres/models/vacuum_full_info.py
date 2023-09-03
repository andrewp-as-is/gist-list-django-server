__all__ = ['SizeCapture']

from django.db import models

class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(ignore_conflicts=True)
        return super().bulk_create(objs,**kwargs)

class SizeCapture(models.Model):
    objects = Manager()

    regclass = models.TextField() # DROP safe (regclass vs oid)
    size_before = models.TextField()
    size_after = models.TextField()
    timestamp = models.TextField()

    class Meta:
        managed = False

