__all__ = ['ApiGraphqlUserGistsPaginationJob']

from django.db import models

class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        kwargs = dict(ignore_conflicts=True) | kwargs
        return super().bulk_create(objs,**kwargs)

class ApiGraphqlUserGistsPaginationJob(models.Model):
    objects = Manager()

    user_id = models.IntegerField(unique=True)

    class Meta:
        managed = False