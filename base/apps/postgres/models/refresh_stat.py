__all__ = ['RefreshStat',]

from django.db import models

class RefreshStat(models.Model):
    schemaname = models.TextField()
    tablename = models.TextField()
    avg_duration = models.FloatField()
    min_duration = models.FloatField()
    max_duration = models.FloatField()
    timestamp = models.IntegerField()

    class Meta:
        managed = False
        ordering = ('schemaname','tablename',)
        unique_together = [('schemaname','tablename',)]

