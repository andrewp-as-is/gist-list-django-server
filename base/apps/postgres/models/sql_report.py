__all__ = ['SqlReport',]

from django.db import models

class SqlReport(models.Model):
    sql = models.TextField()
    duration = models.FloatField()
    timestamp = models.IntegerField()

    class Meta:
        managed = False
        ordering = ('-timestamp',)
