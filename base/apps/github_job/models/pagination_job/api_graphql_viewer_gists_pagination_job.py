__all__ = ['ApiGraphqlViewerGistsPaginationJob']

from django.db import models

from base.apps.django_command_job.utils import create_job


class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(ignore_conflicts=True)
        result = super().bulk_create(objs,**kwargs)
        create_job('github_%s' % __name__.split('.')[-1])
        return result

class ApiGraphqlViewerGistsPaginationJob(models.Model):
    objects = Manager()

    user_id = models.IntegerField(unique=True)

    class Meta:
        managed = False
