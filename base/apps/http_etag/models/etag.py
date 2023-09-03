__all__ = ['Etag',]

from django.db import models

class Etag(models.Model):
    url = models.TextField(unique=True)
    etag = models.TextField()

    class Meta:
        managed = False
