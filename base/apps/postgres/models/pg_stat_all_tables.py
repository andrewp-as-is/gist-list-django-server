__all__ = ['PgStatAllTables']

from django.db import models


class PgStatAllTables(models.Model):
    relid = models.IntegerField(primary_key=True)
    schemaname = models.TextField()
    relname = models.DateTimeField()
    n_live_tup = models.IntegerField()

    class Meta:
        managed = False
