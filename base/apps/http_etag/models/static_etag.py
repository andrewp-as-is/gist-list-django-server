__all__ = ['StaticEtag',]

from django.db import models

class StaticEtag(models.Model):
    url = models.TextField(unique=True)
    etag = models.TextField()

    class Meta:
        managed = False
