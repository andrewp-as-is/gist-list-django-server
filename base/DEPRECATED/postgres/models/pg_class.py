__all__ = ['PgClass']

from django.db import models


class PgClass(models.Model):
    oid = models.AutoField(primary_key=True)
    relnamespace = models.IntegerField()
    relname = models.TextField()
    relkind = models.TextField()
    reltuples = models.IntegerField()

    class Meta:
        managed = False
