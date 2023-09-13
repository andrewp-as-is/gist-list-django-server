__all__ = ['GistOrderJob']

from django.db import models

from base.apps.django_command_job.utils import create_job


class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(ignore_conflicts=True)
        result = super().bulk_create(objs,**kwargs)
        create_job('github_matview_gist_order_job')
        return result

class GistOrderJob(models.Model):
    objects = Manager()

    owner_id = models.IntegerField(unique=True)

    class Meta:
        managed = False
