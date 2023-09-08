__all__ = ['Time']

from django.db import models

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

    url = models.TextField(unique=True)
    timestamp = models.IntegerField()

    class Meta:
        managed = False

