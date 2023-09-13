__all__ = ['RefreshReport',]

from django.db import models

class RefreshReport(models.Model):
    schemaname = models.TextField()
    tablename = models.TextField()
    duration = models.FloatField()
    timestamp = models.IntegerField()

    class Meta:
        managed = False
        ordering = ('-timestamp',)
        unique_together = [('schemaname','tablename',)]

