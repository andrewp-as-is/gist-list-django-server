__all__ = [
    "Etag",
]

from django.db import models


class Etag(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.TextField()
    etag = models.TextField()

    class Meta:
        managed = False
