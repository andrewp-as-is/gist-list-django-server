__all__ = ['PgStatActivity']

from django.db import models


class PgStatActivity(models.Model):
    pid = models.IntegerField(primary_key=True)
    application_name = models.TextField()
    backend_start = models.DateTimeField()
    backend_type = models.TextField()
    query_start = models.DateTimeField()
    state_change = models.DateTimeField()
    state = models.TextField()
    query = models.TextField()

    class Meta:
        managed = False
        ordering = ('pid',)
