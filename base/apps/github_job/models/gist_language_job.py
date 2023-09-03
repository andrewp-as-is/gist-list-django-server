__all__ = ['GistLanguageJob']

from django.contrib.postgres.fields import ArrayField
from django.db import models


class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(ignore_conflicts=True)
        return super().bulk_create(objs,**kwargs)

class GistLanguageJob(models.Model):
    objects = Manager()

    gist_id = models.TextField(unique=True)

    class Meta:
        managed = False
