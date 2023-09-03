__all__ = ['PgNamespace']

from django.db import models


class PgNamespace(models.Model):
    oid = models.IntegerField(primary_key=True)
    nspname = models.TextField()

    class Meta:
        managed = False
