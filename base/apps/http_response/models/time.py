__all__ = ['Time']

from django.db import models

from base.utils import execute_sql

class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(
                update_conflicts=True,
                unique_fields = ['url',],
                update_fields = ['timestamp']
            )
        try:
            return super().bulk_create(objs,**kwargs)
        finally:
            execute_sql('VACUUM http_response.time')


class Time(models.Model):
    objects = Manager()

    url = models.CharField(unique=True,max_length=255)
    timestamp = models.IntegerField()

    class Meta:
        managed = False

