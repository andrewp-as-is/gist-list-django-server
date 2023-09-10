__all__ = ['GistTagJob']

from django.contrib.postgres.fields import ArrayField
from django.db import models

from base.apps.django_command_job.utils import create_job


class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(ignore_conflicts=True)
        result = super().bulk_create(objs,**kwargs)
        create_job('github_%s' % __name__.split('.')[-1])
        return result

class GistTagJob(models.Model):
    objects = Manager()

    gist_id = models.TextField(unique=True)

    class Meta:
        managed = False

