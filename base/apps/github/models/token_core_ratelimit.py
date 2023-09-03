__all__ = ['TokenCoreRatelimit']

from django.db import models

class Manager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        if not kwargs:
            kwargs = dict(
                update_conflicts=True,
                unique_fields = ['token'],
                update_fields = ['ratelimit_remaining','ratelimit_reset']
            )
        return super().bulk_create(objs,**kwargs)

class TokenCoreRatelimit(models.Model):
    objects = Manager()

    token = models.TextField(unique=True)
    ratelimit_remaining = models.IntegerField()
    ratelimit_reset = models.IntegerField()

    class Meta:
        managed = False
