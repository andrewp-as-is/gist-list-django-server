__all__ = [
    "Etag",
]

from django.db import models


class Etag(models.Model):
    url = models.TextField()
    etag = models.TextField()
    created_at = models.FloatField()

    class Meta:
        managed = False
