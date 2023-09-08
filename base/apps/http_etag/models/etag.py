__all__ = ['Etag',]

from django.db import models

from base.utils import execute_sql

class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(
                update_conflicts=True,
                unique_fields = ['url'],
                update_fields = [
                    'etag',
                    'timestamp'
                ]
            )
        try:
            return super().bulk_create(objs,**kwargs)
        finally:
            execute_sql('VACUUM http_etag.etag')


class Etag(models.Model):
    objects = Manager()

    url = models.TextField(unique=True)
    etag = models.TextField()
    timestamp = models.IntegerField()

    class Meta:
        managed = False
