__all__ = ['NewEtag',]

from django.db import models

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
        return super().bulk_create(objs,**kwargs)

class NewEtag(models.Model):
    objects = Manager()

    url = models.TextField(unique=True)
    etag = models.TextField()

    class Meta:
        managed = False
