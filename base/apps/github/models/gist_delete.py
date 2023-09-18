__all__ = ['GistDelete']

from django.db import models

class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(ignore_conflicts=True)
        return super().bulk_create(objs,**kwargs)

class GistDelete(models.Model):
    objects = Manager()

    gist = models.ForeignKey('Gist', related_name='+',on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
